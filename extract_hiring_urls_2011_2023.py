from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def extract_hiring_urls_selenium():
    url = "https://news.ycombinator.com/submitted?id=whoishiring&next=35773707&n=61"

    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Replace with appropriate driver (e.g., Firefox, Edge)

    try:
        # Open the webpage
        driver.get(url)

        all_links = []

        while True:
            # Wait for page content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            # Find all links with "who is hiring" in the text
            links = driver.find_elements(By.XPATH, '//a[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "who is hiring")]')

            # Add found links to the list
            for link in links:
                link_text = link.text
                link_href = link.get_attribute('href')
                if link_href not in [l['url'] for l in all_links]:  # Avoid duplicates
                    all_links.append({"title": link_text, "url": link_href})

            # Check if a "More" link or button exists for pagination
            try:
                more_button = driver.find_element(By.XPATH, '//a[contains(text(), "More")]')
                more_button.click()
                time.sleep(2)  # Allow some time for the next page to load
            except Exception:
                # If "More" button is not found, break the loop
                break

        # Convert the list to JSON
        json_output = json.dumps(all_links, indent=4)

        # Save to a file (optional)
        with open("hiring_urls.json", "w") as f:
            f.write(json_output)

        # Print the JSON output
        print(json_output)

    finally:
        # Close the browser
        driver.quit()

# Call the function
extract_hiring_urls_selenium()
