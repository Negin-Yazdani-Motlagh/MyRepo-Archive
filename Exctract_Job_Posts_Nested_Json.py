import os
import json
from bs4 import BeautifulSoup

# Path to the folder containing HTML files
html_folder = "C:/Users/negin/HTML_Content/HTML_Content"
output_file = "C:/Users/negin/HTML_Content/nested_comments.json"  # Output JSON file

# Nested JSON structure
nested_data = {"YC": {}}

# Process each HTML file
for file_name in os.listdir(html_folder):
    if file_name.endswith(".html"):
        print(f"Processing {file_name}...")
        file_path = os.path.join(html_folder, file_name)

        # Open and parse the HTML file
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            articles = soup.find_all(class_="athing")

            # Extract top-level comments
            top_level_comments = []
            for article in articles:
                commtext = article.find(class_="commtext")
                ind = article.find(class_="ind")
                if commtext and ind and ind.get("indent") == "0":
                    top_level_comments.append(commtext.get_text(strip=True))

            # Add to nested JSON structure
            month = file_name.replace(".html", "")  # Use file name (e.g., "2025-01") as the key
            nested_data["YC"][month] = {
                "comments": top_level_comments,
                "numJobPost": len(top_level_comments),
            }

# Save the nested JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(nested_data, f, indent=4)

print(f"Data saved to {output_file}")
