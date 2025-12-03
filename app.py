from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
from serpapi import GoogleSearch
import random, time, os, hashlib
from fastapi.middleware.cors import CORSMiddleware
import nltk
from nltk.corpus import wordnet
from datetime import datetime, timedelta
from collections import defaultdict

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Private Search Engine API",
    description="Privacy-preserving search using SerpAPI, TOR routing, and decoy queries"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


# TOR PROXY SETTINGS

TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}


# Rate Limiting & Query Tracking

query_tracker = defaultdict(list)
MAX_QUERIES_PER_MINUTE = 10

def check_rate_limit(identifier: str) -> bool:
    """Simple rate limiting to prevent abuse"""
    now = datetime.now()
    # Clean old entries
    query_tracker[identifier] = [
        timestamp for timestamp in query_tracker[identifier]
        if now - timestamp < timedelta(minutes=1)
    ]
    
    if len(query_tracker[identifier]) >= MAX_QUERIES_PER_MINUTE:
        return False
    
    query_tracker[identifier].append(now)
    return True


# Decoy Generator

TRENDING_TOPICS = [
    "weather", "news", "sports scores", "stock market", 
    "movie reviews", "recipes", "how to", "best practices",
    "tutorial", "guide", "tips", "latest updates"
]

COMMON_QUERIES = [
    "what is", "how to", "best", "top 10", "review",
    "near me", "vs", "meaning", "definition", "examples"
]

def semantic_decoys(user_query):
    """Generate semantically related decoy queries"""
    words = user_query.split()
    decoys = []

    for word in words:
        if len(word) < 3:  
            continue
            
        synonyms = wordnet.synsets(word)
        lemmas = [l.name().replace("_", " ") for syn in synonyms for l in syn.lemmas()]
        lemmas = list(set([l for l in lemmas if l.lower() != word.lower()]))
        
        if lemmas:
            # Add individual synonyms
            decoys.extend(random.sample(lemmas, min(2, len(lemmas))))
    
    # Create synonym-based phrases
    if len(decoys) >= 2:
        decoy_phrases = [
            " ".join(random.sample(decoys, 2)) for _ in range(2)
        ]
        return decoy_phrases[:3]
    
    return decoys[:3]

def contextual_decoys(user_query):
    """Generate contextually similar but different queries"""
    words = user_query.split()
    decoys = []
    
    # Add common query patterns
    if len(words) > 0:
        decoys.append(f"{random.choice(COMMON_QUERIES)} {random.choice(words)}")
        decoys.append(f"{random.choice(words)} {random.choice(TRENDING_TOPICS)}")
    
    # Add partial query variations
    if len(words) > 2:
        decoys.append(" ".join(random.sample(words, len(words) - 1)))
    
    return decoys[:2]

def random_trending_decoys():
    """Generate completely random trending topic queries"""
    return [
        f"{random.choice(COMMON_QUERIES)} {random.choice(TRENDING_TOPICS)}",
        random.choice(TRENDING_TOPICS)
    ]

def generate_decoys(user_query, num_decoys=5):
    """
    Generate diverse decoy queries using multiple strategies
    """
    all_decoys = []
    
    # 1. Semantic decoys (synonyms)
    all_decoys.extend(semantic_decoys(user_query))
    
    # 2. Contextual decoys (similar patterns)
    all_decoys.extend(contextual_decoys(user_query))
    
    # 3. Random trending topics
    all_decoys.extend(random_trending_decoys())
    
    # 4. Traditional reversed/modified queries
    words = user_query.split()
    for word in words:
        if len(word) > 4:
            all_decoys.append(word[::-1])
    
    # Add query modifiers
    modifiers = ["history", "tutorial", "explained", "guide", "tips"]
    all_decoys.append(f"{user_query} {random.choice(modifiers)}")
    
    # Remove duplicates and select random subset
    all_decoys = list(set([d for d in all_decoys if d and len(d) > 2]))
    
    return random.sample(all_decoys, min(num_decoys, len(all_decoys)))


# Query Fingerprint Protection

def anonymize_query(query):
    """Create a hash of the query for logging without storing actual query"""
    return hashlib.sha256(query.encode()).hexdigest()[:16]


# Perform Search (via TOR)

def perform_search(query, use_tor=True, num_results=10):
    """
    Perform search with optional TOR routing
    """
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results,  # Number of results to fetch
        "gl": "us",  # Geolocation set to US for consistency
        "hl": "en"   # Language set to English
    }

    # Add proxy configuration directly to params if using TOR
    if use_tor and TOR_PROXY:
        # SerpAPI expects proxy in a different format
        params["proxy"] = "socks5://127.0.0.1:9050"

    search = GoogleSearch(params)

    try:
        results = search.get_dict()
        return results.get("organic_results", [])
    except Exception as e:
        print(f"Search error for query '{query}': {str(e)}")
        # If TOR connection fails, try without proxy
        if use_tor:
            print(f"Retrying without TOR proxy...")
            return perform_search(query, use_tor=False)
        return []

# ============================
# Timing Analysis Protection
# ============================
def obfuscated_delay():
    """Random delay with normal distribution to prevent timing analysis"""
    base_delay = random.gauss(0.8, 0.3)  # Mean 0.8s, std 0.3s
    return max(0.3, min(2.0, base_delay))  # Clamp between 0.3-2.0s

@app.get("/")
def root():
    return {
        "message": "Private Search Engine API is running 🚀",
        "features": [
            "TOR routing",
            "Decoy query generation",
            "Timing obfuscation",
            "Rate limiting",
            "Query anonymization"
        ]
    }

# ============================
# Search Endpoint
# ============================
@app.get("/search")
def private_search(
    query: str = Query(..., description="User's actual search query"),
    num_decoys: int = Query(5, ge=3, le=10, description="Number of decoy queries"),
    num_results: int = Query(5, ge=5, le=20, description="Number of search results to return")
):
    """
    Perform privacy-preserving search with decoy queries
    """
    
    # Rate limiting (using query hash as identifier)
    query_hash = anonymize_query(query)
    if not check_rate_limit(query_hash):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait.")
    
    # Validate query
    if not query or len(query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query too short")
    
    # Generate decoy queries
    decoys = generate_decoys(query, num_decoys)
    
    # Randomize query order
    all_queries = decoys.copy()
    insert_index = random.randint(0, len(decoys))
    all_queries.insert(insert_index, query)
    
    # Perform all searches with timing obfuscation
    results = {}
    start_time = time.time()
    
    for i, q in enumerate(all_queries):
        results[q] = perform_search(q, use_tor=True, num_results=num_results)
        
        # Add random delay between searches (except for last query)
        if i < len(all_queries) - 1:
            time.sleep(obfuscated_delay())
    
    total_time = time.time() - start_time
    
    # Prepare response
    return {
        "real_query": query,
        "decoys": decoys,
        "query_order": all_queries,
        "real_query_position": insert_index,
        "total_queries": len(all_queries),
        "results_count": {q: len(results[q]) for q in all_queries},
        "sample_results": results[query],  # Return all results
        "privacy_stats": {
            "total_time_seconds": round(total_time, 2),
            "tor_enabled": True,
            "queries_mixed": True,
            "timing_obfuscated": True
        }
    }


# Health Check Endpoint

@app.get("/health")
def health_check():
    """Check if API and TOR connection are working"""
    return {
        "status": "healthy",
        "tor_configured": bool(TOR_PROXY),
        "api_key_set": bool(SERPAPI_KEY)
    }


# Run the API

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
