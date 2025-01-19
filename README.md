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
**Purpose**:To extract all "Who is Hiring" posts from a JSON file containing the HTML content of Hacker News pages and save the relevant data (titles, URLs, and source URLs, data) to a new JSON file for further analysis or archiving.
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
 parse_soft_skills_occurrences.py
**Purpose**: The script processes multiple HTML files to extract only the job posts by identifying and isolating top-level comments (posts) using the ind class for indentation. It removes all replies to keep only the main job posts for each file and organizes them into a nested JSON structure.
**Key Functionality**:
- Reads all .html files from a specified directory.
- Skips replies by checking the indent attribute in the ind class.
  
### `Parse_Job_Posts_From_HTML.py`
**Purpose**:The script processes a folder of HTML files containing job postings or comments, extracts top-level comments or job descriptions, and organizes the extracted data into a structured JSON file. It is designed to parse HTML content systematically and save the results for further analysis or visualization.
**Key Functionality**:
- Read and Parse HTML Files.
- Extracts top-level comments (non-reply job descriptions or posts) from elements with specific HTML class names (e.g., class="athing", class="commtext", class="ind").
- Filters comments based on their indentation level (e.g., indent="0").

### `Parse_Job_Posts_From_HTML.json`
**Purpose**:
**Key Functionality**:

### `Parse_total_soft_skills_occurrences.py`
**Purpose**: The script aims to analyze the occurrences of soft skills in job descriptions from a nested JSON file of job posts. It combines data from two sources—a list of soft skills from an Excel file and job post descriptions from a JSON file—and produces a structured summary of soft skill mentions, categorized by time periods (e.g., months).
**Key Functionality**:
- Reads soft skills from an Excel file with multiple columns.
- Compiles a unified set of all soft skills, ensuring there are no duplicates.
- Counts the total number of job posts for each time period.
- Sorts skills by their frequency in descending order for better insights.
  
- ### `Parse_total_soft_skills_occurrences.json`
**Purpose**: This JSON file contains a nested structure summarizing the occurrences of soft skills across different time periods (e.g., months) extracted from job descriptions or posts. It provides insights into which soft skills are most in demand during each period, as well as the total number of job posts analyzed.
**Key Functionality**:
- The root key groups all the data under the label YC (e.g., for Y Combinator job posts or similar sources).
- Each time period (e.g., 2025-01, 2025-02) serves as a nested key.
- Represents data for a specific month or other grouping.
- Each time period contains keys for individual soft skills (e.g., Communication, Collaboration).
- Each time period includes a special key, numJobPost, which represents the total number of job descriptions analyzed for that period.

### `soft_skills_monthly_analysis.py`  
**Purpose**: The script analyzes the monthly occurrence of soft skills in job postings, using a JSON file of job descriptions and an Excel file containing a list of soft skills. It generates a summary of how often specific soft skills are mentioned each month and saves the results for further analysis or visualization.
**Key Functionality**:
- Reads soft skills from an Excel file.
- Consolidates skills from all columns into a unified, de-duplicated set.
- Recursively traverses a nested JSON file containing job postings.
- Extracts all relevant text descriptions (e.g., job descriptions, comments) associated with each month.
- Matches soft skills against job descriptions (case-insensitive).
- Tracks the frequency of each soft skill for every month.
- Adds a numJobPost count to record the total number of job postings analyzed for each month.
  
### `soft_skills_monthly_analysis.json`  
**Purpose**: The JSON file provides a detailed, time-organized summary of soft skill mentions in job postings. It captures the frequency of soft skills mentioned in job descriptions for each month and includes the total number of job postings analyzed, enabling trend analysis and skill demand insights.
**Key Functionality**:
- Each key in the JSON represents a time period (e.g., "January-2025"), grouping all data for that month.
- Lists the soft skills (e.g., "Communication", "Teamwork") and their respective frequencies for each month.
- A special key, numJobPost, is included for each time period, indicating the total number of job descriptions analyzed.
- Provides context for interpreting the soft skill frequencies.

### `visualize_job_postings.py`
**Purpose**:The script visualizes job posting trends over time using data extracted from a soft skills analysis JSON file. It generates a line chart that displays the number of job postings for each month and year, providing insights into hiring trends and activity levels across different periods.
**Key Functionality**:
- Reads the input JSON file containing job posting data (numJobPost) organized by time periods.
- Extracts the numJobPost values and their corresponding time periods from the JSON.
- Converts time periods (e.g., "April-2012") into Python datetime objects for proper chronological sorting.
- X-axis: Time periods (months and years).
- Y-axis: Number of job postings (numJobPost).

### `visualize_job_postings.png`
**Purpose**: The image provides a visual representation of job posting trends over time, displaying the total number of job postings for each month and year. It enables easy identification of hiring patterns, activity levels, and temporal trends in job postings.
**Key Functionality**:
- Represents time periods (e.g., months and years) in chronological order.
- Ensures clarity by formatting dates as "Month Year" (e.g., "Apr 2012").
- Displays the total number of job postings (numJobPost) for each time period.
- Provides a clear measure of hiring activity.

### `soft_skills_ratio_trend_all_months.py`
**Purpose**:This script processes a JSON file (soft_skills_monthly_analysis.json) containing soft skill analysis data and creates a line chart that visualizes the ratio of soft skill mentions to total job postings over time. The chart provides insights into the proportion of job postings emphasizing soft skills during each time period.
**Key Functionality**:
- Reads data from a JSON file (soft_skills_monthly_analysis.json), structured by time periods (e.g., "April-2012") and containing: "numJobPost": Total number of job postings for the period.
- Soft skills (e.g., "Communication", "Collaboration") with their occurrence counts.
- For each time period: Parses the date into a datetime object for proper chronological sorting.
- Retrieves: total_job_posts: Total number of job postings for the period. total_soft_skill_mentions: Sum of all soft skill occurrences in the period. Calculates the ratio of soft skill mentions to total job postings.

### `soft_skills_ratio_trend_all_months.png`
**Purpose**: The chart visually represents the ratio of soft skill mentions to total job postings over time, providing insights into how frequently soft skills are emphasized in job postings during different months and years. It helps identify trends and patterns in the demand for soft skills across the analyzed periods.
**Key Functionality**:
- Time-Based X-Axis: Displays time periods (e.g., months and years) in chronological order.
- Ensures readability by formatting labels as "Month Year" (e.g., "Apr 2012") and rotating them 90° to avoid overlap.
- Connects data points with a smooth line (linestyle='-') to highlight trends.
- Includes markers (o) at each data point for visibility.
  
### `soft_skills_network_analysis.py`
**Purpose**: This script is designed to analyze job postings for sentences containing the term "network" and identify contexts where it relates to soft skills. The goal is to extract and study interpersonal or organizational skills tied to networking from job descriptions.
**Key Functionality**:
- Parses a nested JSON file of job postings to extract textual descriptions.
- Identifies sentences containing the word "network" using regex and filters them for further analysis.
- Outputs the filtered sentences into a JSON file for easier analysis and sharing.








