# BlackOut Search - Quick Start Guide

## What You Need
- **VirtualBox** - Download from: https://www.virtualbox.org/wiki/Downloads
- **The OVA file** - `BlackOut-Search.ova` (provided)
- **SerpAPI Key** - Free from: https://serpapi.com/ (100 searches/month free)

---

## Setup (5 Minutes)

### Step 1: Install VirtualBox
1. Download and install VirtualBox for your operating system
2. Open VirtualBox after installation

### Step 2: Import the VM
1. In VirtualBox, click **File** → **Import Appliance**
2. Click the folder icon and select `BlackOut-Search.ova`
3. Click **Next**, then **Import**
4. Wait 5-10 minutes for the import to complete

### Step 3: Start the VM
1. Select **BlackOut-Search-VM** from the list
2. Click the green **Start** button
3. Wait about 1 minute for Ubuntu to boot
4. You'll see a login screen - **you can minimize this window**

### Step 4: Add Your API Key

**Option A - Easy Method (Command Line):**

On your computer (Windows/Mac), open Terminal/PowerShell and run:

```bash
# Windows PowerShell
ssh vagrant@localhost -p 2222
# Password: vagrant

# Once logged in:
cd ~/blackout-search
nano .env

# Type this line:
SERPAPI_KEY=paste_your_api_key_here

# Save and exit:
# Press Ctrl+X, then Y, then Enter

# Restart the backend:
sudo systemctl restart blackout-backend

# Exit SSH:
exit
```

**Option B - If SSH doesn't work:**

Click on the VM window to access the console, then:
```bash
# Login with:
Username: vagrant
Password: vagrant

# Edit the config:
cd ~/blackout-search
nano .env

# Add your key:
SERPAPI_KEY=your_key_here

# Save: Ctrl+X, Y, Enter

# Restart:
sudo systemctl restart blackout-backend
```

---

## Using BlackOut Search

### Open the Application

On your computer, open any web browser and go to:

```
http://localhost:8080
```

### How to Search

1. **Type your search query** (at least 2 characters)
2. **Select number of results** from the dropdown (5, 10, 15, or 20)
3. **Click the search button** or press Enter
4. **Watch the Privacy Shield** section show:
   - 🎭 5 decoy queries being sent
   - 🎯 Your real query hidden among them
   - 🛡️ Privacy statistics (TOR, timing obfuscation)
5. **View results** below the privacy shield

### What You're Seeing

The **Privacy Shield** shows how your privacy is protected:
- **Decoy Queries**: Fake searches that hide your real search
- **Query Position**: Where your real query is in the mix
- **TOR Routing**: All searches go through anonymous TOR network
- **Timing Obfuscation**: Random delays prevent pattern detection

---

## Troubleshooting

### Can't Access http://localhost:8080

**Solution 1: Wait a bit**
The VM takes 1-2 minutes after startup for services to start. Wait and try again.

**Solution 2: Check services**
```bash
ssh vagrant@localhost -p 2222
# Password: vagrant

# Check if running:
sudo systemctl status blackout-backend
sudo systemctl status blackout-frontend

# If not running, start them:
sudo systemctl start blackout-backend
sudo systemctl start blackout-frontend

exit
```

**Solution 3: Restart the VM**
1. In VirtualBox: Select the VM → **Machine** → **Reset**
2. Wait 1-2 minutes
3. Try http://localhost:8080 again

### "Query too short" Error

You need at least 2 characters. Try searching for:
- "test"
- "weather"
- "news"

### "No results found" or Only 2 Results

**Cause:** SerpAPI free tier limits (100 searches/month, limited results per search)

**Check your quota:**
1. Go to https://serpapi.com/
2. Login to your account
3. Check your dashboard for remaining searches

### "Error connecting to backend"

**Check if backend is healthy:**

Open in browser: http://localhost:8000/health

Should show: `{"status":"healthy","tor_configured":true,"api_key_set":true}`

If you get an error:
```bash
ssh vagrant@localhost -p 2222
sudo systemctl restart blackout-backend
exit
```

---

## Stopping and Starting

### Stop the VM (When Done)

**Option 1: Save State (Faster next startup)**
1. In VirtualBox, select the VM
2. Click **Machine** → **Close** → **Save the machine state**

**Option 2: Power Off**
1. Click **Machine** → **Close** → **Power Off**

### Start the VM Again

1. In VirtualBox, select **BlackOut-Search-VM**
2. Click **Start**
3. Wait 1-2 minutes
4. Open http://localhost:8080

---

## Testing the Privacy Features

### Example Search Flow

1. Search for: **"climate change"**
2. Observe the Privacy Shield showing:
   ```
   🎭 Decoy: "weather tutorial"
   🎭 Decoy: "environment guide"
   🎯 Your Query: "climate change"  ← Hidden in position 3 of 6
   🎭 Decoy: "global news"
   🎭 Decoy: "temperature data"
   🎭 Decoy: "ecological tips"
   ```
3. Notice:
   - Total Queries: 6 (1 real + 5 decoys)
   - TOR Routing: ✓ Enabled
   - Timing Obfuscated: ✓ Yes
4. View your search results below

### What This Means

An observer (like Google or your ISP) sees:
- 6 different search queries
- Can't tell which one is your real search
- All coming through TOR (different IP address)
- Random timing makes correlation difficult

**Your privacy is protected!** 🛡️

---

## System Requirements

- **VirtualBox**: Version 6.1 or higher
- **RAM**: 4GB minimum (2GB for VM + 2GB for host)
- **Disk Space**: 5GB free
- **Internet**: Required for searches
- **Operating System**: Windows, macOS, or Linux

---

## Quick Reference

| What | Where |
|------|-------|
| **Frontend** | http://localhost:8080 |
| **Backend Health** | http://localhost:8000/health |
| **VM Login** | vagrant / vagrant |
| **SSH Access** | `ssh vagrant@localhost -p 2222` |
| **Min Search Length** | 2 characters |

---

## Getting Help

### Check Service Status
```bash
ssh vagrant@localhost -p 2222
sudo systemctl status blackout-backend
sudo journalctl -u blackout-backend -n 20
exit
```

### View Recent Logs
```bash
ssh vagrant@localhost -p 2222
sudo journalctl -u blackout-backend -f
# Press Ctrl+C to exit
exit
```

### Full Reset
If nothing works, restart the VM:
1. VirtualBox → Select VM → **Machine** → **Reset**
2. Wait 2 minutes
3. Try http://localhost:8080

---

## That's It!

You're now searching privately with BlackOut Search! 

**Enjoy anonymous searching!** 🔍🛡️