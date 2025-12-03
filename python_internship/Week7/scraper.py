import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor # For Concurrency

# --- 1. CONFIGURATION ---
TARGET_URLS = [
    "https://www.cnn.com/",
    "https://www.bbc.com/news",
    "https://www.theguardian.com/international",
    "https://www.reuters.com/",
    "https://www.nytimes.com/",
    "https://www.washingtonpost.com/",
    "https://www.aljazeera.com/"
]
CONCURRENT_WORKERS = 5 # Number of threads/processes to use

# --- 2. CORE SCRAPING FUNCTION ---
def scrape_headline(url):
    """Fetches a URL and extracts a headline."""
    print(f"-> Starting scrape: {url}")
    
    # Store the result locally to avoid polluting the global results list directly
    result = None
    
    try:
        # 10-second timeout for the request
        response = requests.get(url, timeout=10) 
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- Parsing Logic ---
            # Try finding common headline tags (h1, h2)
            headline_tag = soup.find('h1') or soup.find('h2') 
            
            if headline_tag:
                result = headline_tag.get_text(strip=True)
            else:
                result = "Headline not found (Selector failure)"

            print(f"<- Success scraping {url}.")
            
        else:
            result = f"Failed to fetch. Status: {response.status_code}"
            print(f"<- Failed to fetch {url}. Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        result = f"Error: {e.__class__.__name__}"
        print(f"<- Error scraping {url}: {result}")
        
    return (url, result) # Return the URL and its result

# --- 3. SEQUENTIAL EXECUTION ---
def sequential_run(urls):
    """Scrapes URLs sequentially (one after the other)."""
    start_time = time.perf_counter()
    print("\n" + "="*15 + " Sequential Run Started " + "="*15)
    
    results = []
    for url in urls:
        # Calls the function and waits for it to finish before the next iteration
        results.append(scrape_headline(url))
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    print("\n" + "="*15 + " Sequential Run Finished " + "="*15)
    print(f"Sequential Run Total Time: {duration:.4f} seconds")
    return duration, results

# --- 4. CONCURRENT EXECUTION (THREADING) ---
def concurrent_run_threading(urls):
    """Scrapes URLs concurrently using Threading (ideal for I/O-bound tasks)."""
    start_time = time.perf_counter()
    print("\n" + "="*12 + f" Concurrent Run (Threading) Started with {CONCURRENT_WORKERS} workers " + "="*12)
    
    # ThreadPoolExecutor manages a pool of threads
    # 


    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        # executor.map submits all the functions and arguments at once
        results = list(executor.map(scrape_headline, urls))
        
    end_time = time.perf_counter()
    duration = end_time - start_time
    print("\n" + "="*12 + " Concurrent Run (Threading) Finished " + "="*12)
    print(f"Concurrent Run Total Time: {duration:.4f} seconds")
    return duration, results

# --- 5. MAIN EXECUTION & COMPARISON ---
if __name__ == "__main__":
    
    # 1. Run Sequential
    sequential_time, sequential_results = sequential_run(TARGET_URLS)
    
    # 2. Run Concurrent (Using Threading)
    concurrent_time, concurrent_results = concurrent_run_threading(TARGET_URLS)
    
    # 3. Final Comparison
    print("\n" + "#"*55)
    print("### RESULTS SUMMARY ###")
    print(f"Total URLs Scraped: {len(TARGET_URLS)}")
    print("-" * 55)
    print(f"Sequential Time: {sequential_time:.4f} seconds")
    print(f"Concurrent Time: {concurrent_time:.4f} seconds")
    print("-" * 55)
    
    if concurrent_time < sequential_time:
        speed_up = sequential_time / concurrent_time
        print(f"Speed-up Achieved! Concurrent run was {speed_up:.2f}x faster.")
    else:
        print("No significant speed-up observed. Concurrent run was slower or similar.")
        
    # Optional: Display the first few results
    print("\nSample Results (from Concurrent Run):")
    for url, headline in concurrent_results[:3]:
        print(f"- {url}: {headline[:80]}...")