 1. import requests
 2. import time
 3. import json
 4. import os
 5. from requests.adapters import HTTPAdapter
 6. from urllib3.util.retry import Retry
 7.  
 8. # Input JSON and output directory
 9. input_file = "Who_is_hiring.json"
10. output_dir = "HTML_Content"
11. os.makedirs(output_dir, exist_ok=True)
12.  
13. # Headers to mimic a browser
14. headers = {
15.     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36"
16. }
17.  
18. # Retry and session setup
19. retry_strategy = Retry(
20.     total=5,  # Retry up to 5 times
21.     backoff_factor=2,  # Exponential backoff (2s, 4s, 8s, etc.)
22.     status_forcelist=[403, 429, 500, 502, 503, 504],  # Retry on these status codes
23.     allowed_methods=["GET"]  # Corrected argument
24. )
25. adapter = HTTPAdapter(max_retries=retry_strategy)
26. session = requests.Session()
27. session.mount("http://", adapter)
28. session.mount("https://", adapter)
29.  
30. # Fetch and save HTML content for each URL
31. with open(input_file, 'r', encoding='utf-8') as file:
32.     data = json.load(file)
33.  
34. for entry in data:
35.     title = entry.get('title', 'Unknown Title')
36.     url = entry.get('url')
37.  
38.     if not url:
39.         print(f"Skipping entry with missing URL: {entry}")
40.         continue
41.  
42.     try:
43.         print(f"Fetching: {url}")
44.         response = session.get(url, headers=headers, timeout=15)
45.         response.raise_for_status()
46.  
47.         html_content = response.text
48.         safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
49.         file_name = f"{safe_title}.html"
50.         output_path = os.path.join(output_dir, file_name)
51.  
52.         with open(output_path, 'w', encoding='utf-8') as output_file:
53.             output_file.write(html_content)
54.  
55.         print(f"Saved HTML content for '{title}' to {output_path}")
56.         time.sleep(2)  # Delay to prevent rate limiting
57.     except requests.exceptions.RequestException as e:
58.         print(f"Failed to fetch or save HTML for '{title}' from {url}: {e}")
59.  
