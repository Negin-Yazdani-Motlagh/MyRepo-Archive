 1. import requests
 2. import json
 3.  
 4. # List of URLs to extract HTML from
 5. urls = [
 6.     "https://news.ycombinator.com/submitted?id=whoishiring",
 7.     "https://news.ycombinator.com/submitted?id=whoishiring&next=39562986&n=31",
 8.     "https://news.ycombinator.com/submitted?id=whoishiring&next=35773707&n=61",
 9.     "https://news.ycombinator.com/submitted?id=whoishiring&next=31947297&n=91",
10.     "https://news.ycombinator.com/submitted?id=whoishiring&next=28380661&n=121",
11.     "https://news.ycombinator.com/submitted?id=whoishiring&next=24969524&n=151",
12.     "https://news.ycombinator.com/submitted?id=whoishiring&next=22225313&n=181",
13.     "https://news.ycombinator.com/submitted?id=whoishiring&next=19543939&n=211",
14.     "https://news.ycombinator.com/submitted?id=whoishiring&next=17205866&n=241",
15.     "https://news.ycombinator.com/submitted?id=whoishiring&next=14901314&n=271",
16.     "https://news.ycombinator.com/submitted?id=whoishiring&next=12627853&n=301",
17.     "https://news.ycombinator.com/submitted?id=whoishiring&next=10655741&n=331",
18.     "https://news.ycombinator.com/submitted?id=whoishiring&next=8822808&n=361",
19.     "https://news.ycombinator.com/submitted?id=whoishiring&next=7162197&n=391",
20.     "https://news.ycombinator.com/submitted?id=whoishiring&next=4857717&n=421",
21.     "https://news.ycombinator.com/submitted?id=whoishiring&next=2949790&n=451"
22. ]
23.  
24. # Dictionary to store results
25. results = []
26.  
27. # Loop through each URL, fetch HTML, and save to results
28. for url in urls:
29.     try:
30.         response = requests.get(url, timeout=10)
31.         response.raise_for_status()  # Raise an error for bad status codes
32.         html_content = response.text
33.         results.append({"url": url, "html": html_content})
34.     except requests.RequestException as e:
35.         print(f"Failed to fetch {url}: {e}")
36.         results.append({"url": url, "html": None, "error": str(e)})
37.  
38. # Save results to JSON file
39. output_file = "urls_html_content.json"
40. with open(output_file, 'w', encoding='utf-8') as file:
41.     json.dump(results, file, ensure_ascii=False, indent=4)
42.  
43. print(f"HTML content saved to {output_file}")
44.  
