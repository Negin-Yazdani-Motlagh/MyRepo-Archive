import json
from bs4 import BeautifulSoup

def extract_who_is_hiring(json_file, output_file):
    extracted_data = []

    # Load the JSON file containing HTML content
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Iterate through each entry in the JSON file
    for entry in data:
        url = entry["url"]
        html_content = entry["html"]

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all titlelines
        titlelines = soup.find_all("span", class_="titleline")
        for titleline in titlelines:
            link = titleline.find("a")
            if link:
                title = link.text.strip()
                # Check if the title contains "who is hiring" (case-insensitive)
                if "who is hiring" in title.lower():
                    post_url = f"https://news.ycombinator.com/{link['href']}"
                    extracted_data.append({"title": title, "url": post_url, "source_url": url})

    # Save the extracted data to a JSON file
    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(extracted_data, output, indent=4)

    print(f"Extracted data saved to {output_file}")

# Specify the input JSON file and the output JSON file
input_json_file = "HTML_All_pages.json"  # Replace with your JSON file
output_json_file = "Who_is_hiring.json"  # Output JSON file for extracted data

# Call the function
extract_who_is_hiring(input_json_file, output_json_file)
