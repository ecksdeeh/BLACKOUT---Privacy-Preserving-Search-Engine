# BlackOut Search: Privacy-Preserving Search Engine

## Abstract

BlackOut Search is a privacy-preserving search engine implementation that employs query obfuscation techniques to protect user privacy during web searches. The system utilizes decoy query generation, TOR routing, and timing obfuscation to prevent search engines and network observers from building accurate user profiles. This implementation demonstrates practical privacy-enhancing technologies (PETs) for web search scenarios.

## 1. Introduction

Modern search engines collect extensive user data through search queries, enabling detailed user profiling and behavioral tracking [1]. BlackOut Search addresses these privacy concerns by implementing a multi-layered privacy protection system that includes:

- **Decoy Query Generation**: Semantic and contextual fake queries mixed with real searches
- **TOR Network Routing[5]**: Anonymous network routing to hide user IP addresses
- **Timing Obfuscation**: Randomized delays to prevent timing-based correlation attacks
- **Query Anonymization**: Cryptographic hashing to prevent server-side tracking

## 2. System Architecture

### 2.1 Backend Components

The backend is built using FastAPI and implements the following privacy mechanisms:

1. **Query Obfuscation Module**: Generates semantically related decoy queries using WordNet
2. **Search Proxy**: Routes all queries through the TOR network
3. **Rate Limiter**: Prevents abuse and ensures system stability
4. **Privacy Statistics Tracker**: Monitors and reports privacy metrics

### 2.2 Frontend Components

The web interface provides:

1. **Privacy Shield Display**: Real-time visualization of active privacy protections
2. **Decoy Query Monitor**: Shows all queries being sent (real and decoys)
3. **Privacy Metrics Dashboard**: Displays TOR status, timing obfuscation, and query mixing
4. **Search Results Interface**: Standard search result display with privacy indicators

## 3. Installation and Setup

### 3.1 Prerequisites

- Python 3.8 or higher
- Node.js and npm (optional, for development)
- TOR Browser or standalone TOR service
- SerpAPI account with API key

### 3.2 Environment Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/ecksdeeh/BLACKOUT---Privacy-Preserving-Search-Engine.git
cd blackout-search
```

#### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
google-search-results==2.4.2
nltk==3.8.1
requests[socks]==2.31.0
```

#### Step 3: Download NLTK Data

```python
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

#### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
SERPAPI_KEY=your_serpapi_key_here
```

To obtain a SerpAPI key:
1. Visit https://serpapi.com/
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Paste it into the `.env` file

### 3.3 TOR Configuration

#### Option 1: TOR Browser (Easiest)

1. Download TOR Browser from https://www.torproject.org/
2. Launch TOR Browser(You only need this browser open, you can use any browser for the html page.)
3. TOR proxy will automatically run on `127.0.0.1:9050`

#### Option 2: Standalone TOR Service

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tor
sudo service tor start
```

**On macOS (using Homebrew):**
```bash
brew install tor
brew services start tor
```

**On Windows:**
1. Download TOR Expert Bundle from https://www.torproject.org/download/tor/
2. Extract to a directory
3. Run `tor.exe`

**Verify TOR is running:**
```bash
curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip
```

## 4. Running the Application

### 4.1 Start the Backend Server

```bash
python app.py
```

The API server will start on `http://127.0.0.1:8000`

**Verify backend is running:**
```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "tor_configured": true,
  "api_key_set": true
}
```

### 4.2 Start the Frontend

Open `index.html` in a web browser:

```bash
# On macOS
open index.html

# On Linux
xdg-open index.html

# On Windows
start index.html
```

Alternatively, use a simple HTTP server:

```bash
# Python 3
python -m http.server 8080

# Then navigate to http://localhost:8080
```

### 4.3 Using the Application

1. Enter a search query in the search box
2. Select desired number of results (5, 10, 15, or 20)(Certain queries will retrieve less than 5 results, due to SERPAPI Limitations)
3. Click the search button or press Enter
4. Observe the Privacy Shield showing:
   - All decoy queries being sent
   - Your real query mixed among decoys
   - Privacy statistics (TOR status, timing obfuscation)
5. View search results below the privacy shield

## 5. API Documentation

### 5.1 Endpoints

#### GET /search

Performs a privacy-preserving search with decoy queries.

**Parameters:**
- `query` (string, required): The user's search query
- `num_decoys` (int, optional): Number of decoy queries (3-10, default: 5)
- `num_results` (int, optional): Number of results to return (5-20, default: 10)

**Response:**
```json
{
  "real_query": "string",
  "decoys": ["string"],
  "query_order": ["string"],
  "real_query_position": 0,
  "total_queries": 6,
  "results_count": {},
  "sample_results": [],
  "total_results_returned": 10,
  "privacy_stats": {
    "total_time_seconds": 5.23,
    "tor_enabled": true,
    "queries_mixed": true,
    "timing_obfuscated": true
  }
}
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "tor_configured": true,
  "api_key_set": true
}
```

## 6. Privacy Features

### 6.1 Decoy Query Generation

The system employs multiple strategies for generating realistic decoy queries [2]:

1. **Semantic Decoys**: Using WordNet to generate synonymous queries
2. **Contextual Decoys**: Creating queries with similar patterns and structure
3. **Trending Topics**: Mixing in common search patterns
4. **Query Modifiers**: Adding prefixes like "how to" or suffixes like "tutorial"

### 6.2 Timing Obfuscation

To prevent timing correlation attacks [3], the system implements:

- Gaussian-distributed random delays (μ=0.8s, σ=0.3s)
- Delay range clamped between 0.3-2.0 seconds
- Consistent timing across all queries (real and decoy)

### 6.3 Rate Limiting

Implements a token bucket algorithm with:
- Maximum 10 queries per minute per user
- Rolling window of 60 seconds
- Query fingerprinting using SHA-256 hashing

## 7. Security Considerations

### 7.1 Threat Model

**Adversaries:**
- Search engine providers attempting to profile users
- Network observers conducting traffic analysis
- Third-party trackers monitoring search behavior

**Assumptions:**
- TOR network is not compromised
- SerpAPI does not perform advanced correlation attacks
- Local machine is not compromised

### 7.2 Known Limitations

1. **SerpAPI Dependency**: Reliance on third-party API may introduce privacy risks
2. **Free Tier Limits**: API restrictions may limit effectiveness
3. **TOR Exit Nodes**: Exit node operators could potentially observe traffic
4. **Browser Fingerprinting**: Frontend does not protect against browser-level tracking

## 8. Troubleshooting

### 8.1 Common Issues

**Issue: "AttributeError: 'GoogleSearch' object has no attribute 'session'"**

Solution: Updated to use SerpAPI's native proxy configuration. Ensure you're using the latest version of the code.

**Issue: Only 2 results showing**

Possible causes:
- SerpAPI free tier limitation (typically 100 searches/month, limited results)
- TOR proxy interfering with API requests
- Invalid API key or quota exceeded

Solutions:
1. Check SerpAPI dashboard for quota limits
2. Temporarily disable TOR: Set `use_tor=False` in the search endpoint
3. Verify API key is correct in `.env` file

**Issue: TOR connection failed**

Solutions:
1. Verify TOR is running: `curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip`
2. Restart TOR service
3. Check firewall settings allow port 9050

**Issue: CORS errors in browser**

Solution: Use a local HTTP server instead of opening HTML directly:
```bash
python -m http.server 8080
```

### 8.2 Debugging

Enable debug mode by checking:

1. **Backend Console**: Shows query counts and API responses
2. **Browser Console** (F12): Shows frontend data and errors
3. **Network Tab**: Monitor API calls and responses

## 9. Performance Metrics

Typical performance characteristics:

- **Query latency**: 4-8 seconds (depends on number of decoys and TOR)
- **Bandwidth**: ~50-100KB per search (varies with result count)
- **Privacy overhead**: 5-10x slower than direct search (due to decoys + TOR)

## 10. Future Enhancements

Potential improvements for future versions:

1. **Local Search Engine**: Implement direct HTML scraping to eliminate SerpAPI dependency
2. **Distributed Proxy Network**: Use multiple proxy sources beyond TOR
3. **Machine Learning Decoys**: Generate more realistic decoys using language models
4. **Differential Privacy**: Add noise to search patterns using differential privacy techniques [4]
5. **Browser Extension**: Package as a browser extension for easier deployment
6. **Peer-to-Peer Architecture**: Distribute queries across multiple users

## 11. Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 12. Acknowledgments

This project implements privacy-preserving techniques inspired by academic research in query obfuscation and anonymous communications. Special thanks to the TOR Project and the privacy research community, as well as all of the people who researched all of these important privacy-related topics.

## References

[1] A. Wills and M. Tatar. 2012. An analysis of search engine privacy. In *Proceedings of the 2012 ACM Conference on Computer and Communications Security* (CCS '12). Association for Computing Machinery, New York, NY, USA, 895–907. https://doi.org/10.1145/2382196.2382289

[2] D. Rebollo-Monedero, J. Forné, A. Solanas, and T. Martínez-Ballesté. 2010. Private location-based information retrieval through user collaboration. *Computer Communications* 33, 6 (2010), 762–774. https://doi.org/10.1016/j.comcom.2009.11.024

[3] X. Luo, P. Zhou, E. W. Chan, W. Lee, R. K. Chang, and R. Perdisci. 2011. HTTPOS: Sealing information leaks with browser-side obfuscation of encrypted flows. In *Proceedings of the 18th Annual Network and Distributed System Security Symposium* (NDSS '11). Internet Society, San Diego, CA, USA. https://www.ndss-symposium.org/wp-content/uploads/2017/09/luo.pdf

[4] C. Dwork and A. Roth. 2014. The algorithmic foundations of differential privacy. *Foundations and Trends in Theoretical Computer Science* 9, 3-4 (2014), 211–407. https://doi.org/10.1561/0400000042

[5] R. Dingledine, N. Mathewson, and P. Syverson. 2004. Tor: The second-generation onion router. In *Proceedings of the 13th USENIX Security Symposium*. USENIX Association, Berkeley, CA, USA, 303–320. https://www.usenix.org/legacy/publications/library/proceedings/sec04/tech/full_papers/dingledine/dingledine.pdf



## 13. Related Work

[6] H. Nissenbaum and J. Howe. 2009. TrackMeNot: Reclaiming Search Privacy in the Age of Personalized Search. In Proceedings of the 2009 International Conference on Social Computing (SocialCom ’09). IEEE, New York, NY, USA, 588–593. https://doi.org/10.1109/SocialCom.2009.33

[7] J. L. Domingo-Ferrer, A. Solanas, and J. Castellà-Roca. 2009. Hiding Information for Privacy Protection: A Survey. Computer Communications 32, 12 (2009), 1631–1647. https://doi.org/10.1016/j.comcom.2009.05.002
---

**Project Status**: Active Development  
**Version**: 0.99.0(BETA)  
**Last Updated**: December 2025  
**Maintainers**: [Adonnis Price, Amir Walker, Tyree Robinson, Fortune Uwaoma]  
**Contact**: [adpri4@morgan.edu, fouwa1@morgan.edu, tyrob14@morgan.edu, amwal17@morgan.edu]
