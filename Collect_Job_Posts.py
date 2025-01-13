import json
from bs4 import BeautifulSoup
import httpx
import requests
import time

# URL of the target webpage
url = "https://news.ycombinator.com/item?id=42297424"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Step 1: Try fetching with `httpx` and headers
def fetch_with_httpx():
    for i in range(3):  # Retry 3 times
        try:
            print(f"Attempt {i + 1} with httpx...")
            response = httpx.get(url, headers=headers)
            if response.status_code == 200:
                print("Fetched successfully with httpx!")
                return response.content
            else:
                print(f"Failed with status code: {response.status_code}")
        except httpx.RequestError as e:
            print(f"Httpx request error: {e}")
        time.sleep(2 ** i)  # Exponential backoff
    return None

# Step 2: Fallback to `requests` if `httpx` fails
def fetch_with_requests():
    try:
        print("Attempting with requests...")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Fetched successfully with requests!")
            return response.content
        else:
            print(f"Failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Requests library error: {e}")
    return None

# Main function to fetch the webpage
def fetch_webpage():
    # Try httpx first
    content = fetch_with_httpx()
    if content:
        return content

    # Fallback to requests
    content = fetch_with_requests()
    if content:
        return content

    # Raise an exception if all methods fail
    raise Exception("Failed to fetch the webpage after all attempts.")

# Step 3: Parse and process the content
try:
    yc_web_page = fetch_webpage()
    soup = BeautifulSoup(yc_web_page, "html.parser")
    articles = soup.find_all(class_="athing")

    # Process top-level comments based on indentation
    top_level_comments = []
    for article in articles:
        commtext = article.find(class_="commtext")
        ind = article.find(class_="ind")
        if commtext and ind and ind.get("indent") == "0":
            top_level_comments.append({"comment": commtext.get_text(strip=True)})

    # Output results in JSON format
    result = {
        "url": url,
        "total_comments": len(top_level_comments),
        "comments": top_level_comments,
    }

    print(json.dumps(result, indent=4))  # Pretty print the JSON

except Exception as e:
    print(f"Error: {e}")
