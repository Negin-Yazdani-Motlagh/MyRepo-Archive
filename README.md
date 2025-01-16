# YC-job-posts Repository

This repository contains Python scripts to extract and analyze job postings data from Hacker News's "Who is Hiring" posts. Below is a summary of each file and its functionality.
## Python Files and Their Functionalities

### `Fetch_html_from_urls.py`
**Purpose**:Fetches and stores HTML content from a list of predefined URLs for analysis or archiving.
**Key Functionality**:
- Automates the process of collecting HTML data from multiple web pages.
- Handles HTTP errors and timeouts gracefully, logging errors for failed requests.
- Saves the HTML content along with associated metadata (URL and error details) in a structured JSON file.
### `Fetch_html_from_urls.json`
**Purpose**:Stores the results of the fetch_html_from_urls.py script, containing the HTML content and metadata for each processed URL.
**Key Functionality**:
- Provides a detailed log of successful and failed URL requests.
- Allows easy parsing and analysis of the collected HTML content and errors.
- Can be used to troubleshoot network issues or analyze the structure of the retrieved webpages.
### `Extract_who_is_hiring_pages.py`
**Purpose**:To extract all "Who is Hiring" posts from a JSON file containing the HTML content of Hacker News pages and save the relevant data (titles, URLs, and source URLs) to a new JSON file for further analysis or archiving.
**Key Functionality**:
- Reads a JSON file with webpage URLs and HTML content.
- Parses HTML to find posts titled "Who is Hiring" (case-insensitive).
- Extracts post titles, direct URLs, and source page URLs.
- Saves the extracted data to a new JSON file.
### `Extract_who_is_hiring_pages.json`
**Purpose**:To store the extracted data of "Who is Hiring" posts, including their titles, direct URLs, and source page URLs, from the processed HTML content.
**Key Functionality**:
- Contains structured data with fields: title, url (direct post URL), and source_url (page from which the post was extracted).
- Serves as the output of the Extract_who_is_hiring_posts.py script.
- Enables easy access to filtered "Who is Hiring" posts for analysis or archiving.
### `Fetch_HTML_Who_Is_Hiring_Pages_Individually.py`
**Purpose**:To fetch and save the HTML content of webpages specified in a JSON file.
Each webpage's content is stored as an individual HTML file in a specified directory for offline use, analysis, or archival.
**Key Functionality**:
- Reads a JSON file with title and url fields.
- Fetches HTML content for each URL using HTTP requests with retry and backoff.
- Saves the HTML content as individual files in the HTML_Content directory, named based on sanitized titles.
### `Fetch_HTML_Who_Is_Hiring_Pages_Individually.zip`
**Purpose**:To fetch and save the HTML content of individual "Who is Hiring" pages specified in a JSON file. This tool is designed to archive or analyze these pages offline.
**Key Functionality**:
- Reads a JSON file containing title and url fields for "Who is Hiring" pages.
- Fetches HTML content for each URL using HTTP requests with retry and backoff strategies.
- Saves the HTML content as individual files in a designated directory, named based on sanitized titles.
### `Parse_Job_Posts_From_HTML.py`
- **Purpose**: The script processes multiple HTML files to extract only the job posts by identifying and isolating top-level comments (posts) using the ind class for indentation. It removes all replies to keep only the main job posts for each file and organizes them into a nested JSON structure.
- - **Key Functionality**:
  - Reads all .html files from a specified directory.
  - Skips replies by checking the indent attribute in the ind class.



