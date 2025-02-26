import json
import pandas as pd
import re

# File Paths
input_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_Nested_Job_Posts.json"
output_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Extracted_Job_Posts.xlsx"

# **🔹 Updated Extraction Patterns**
patterns = {
    "Location": r"(?i)\b(?:located in|based in|remote|onsite|work from|working from|hybrid|ONSITE|REMOTE \(US Only\)|US timezones|Onsite \(.*?\)|remote \(.*?\)|open to remote|flexible location|work from anywhere|HQ in|office in)\s*[:,-]?\s*([A-Za-z\s,()-]+)",
    "Salary": r"(?i)(?:\$\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?(?:-\$\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?)?)",
    "Experience": r"(?i)(\b\d{1,2}\s*(?:\+|-|to)?\s*\d{0,2}\s*(?:years?|yrs|y/o/e|experience)?\b)",
    "Job Title": r"(?i)(?:hiring|join|looking for|we are hiring|position:|role:|opening for|engineer|developer|intern|manager|lead|senior|founding|specialist|analyst|principal|director|VP|fullstack|backend|frontend|ML engineer|data scientist|software architect|security engineer|mobile engineer|cloud engineer|SRE|machine learning scientist|AI researcher|UX designer|product manager|solutions architect|QA engineer|DevOps engineer|embedded systems engineer)\s+([\w\s\-/]+)"
}

# **🔹 Storage for Extracted Job Data**
extracted_jobs = []

# **🔹 Load JSON Data**
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# **🔹 Process Each Job Post**
for category, year_data in data.items():
    for year_month, details in sorted(year_data.items(), key=lambda x: pd.to_datetime(x[0], errors="coerce")):
        # Extract Year & Month
        match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", year_month)
        extracted_month, extracted_year = match.groups() if match else ("Unknown", "Unknown")

        for post in details.get("comments", []):  # Extract job descriptions
            extracted_info = {
                "Year": extracted_year,
                "Month": extracted_month,
                "Job Post": post[:500].strip()  # Limit job post text to 500 characters
            }

            # **🔹 Extract Details Using Patterns**
            for key, pattern in patterns.items():
                matches = re.findall(pattern, post)

                # **🔹 Handling for Different Fields**
                if key == "Salary":
                    valid_salaries = [s for s in matches if "$" in s or "K" in s or "%" in s]
                    extracted_info[key] = ", ".join(valid_salaries) if valid_salaries else "Not Specified"

                elif key == "Experience":
                    valid_experience = [s for s in matches if "year" in s.lower() or "yrs" in s.lower()]
                    extracted_info[key] = ", ".join(valid_experience) if valid_experience else "Not Specified"

                elif key == "Location":
                    location_list = [place.strip() for place in matches if len(place.strip()) > 3]
                    extracted_info[key] = ", ".join(set(location_list)) if location_list else "Not Specified"

                elif key == "Job Title":
                    extracted_info[key] = matches[0] if matches else "Not Specified"

                else:
                    extracted_info[key] = ", ".join(set(matches)) if matches else "Not Specified"

            extracted_jobs.append(extracted_info)

# **🔹 Convert Data to DataFrame & Sort**
df = pd.DataFrame(extracted_jobs)

# **Ensure Year & Month are in Order**
df["Year"] = df["Year"].astype(str)
df["Month"] = pd.Categorical(df["Month"], 
    categories=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 
    ordered=True)
df = df.sort_values(by=["Year", "Month"])

# **🔹 Save to Excel**
df.to_excel(output_file, index=False)

print(f"✅ Extracted job details saved to: {output_file}")
import json
import pandas as pd
import re

# File Paths
input_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_Nested_Job_Posts.json"
output_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Extracted_Job_Posts.xlsx"

# **🔹 Updated Extraction Patterns**
patterns = {
    "Location": r"(?i)\b(?:located in|based in|remote|onsite|work from|working from|hybrid|ONSITE|REMOTE \(US Only\)|US timezones|Onsite \(.*?\)|remote \(.*?\)|open to remote|flexible location|work from anywhere|HQ in|office in)\s*[:,-]?\s*([A-Za-z\s,()-]+)",
    "Salary": r"(?i)(?:\$\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?(?:-\$\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?)?)",
    "Experience": r"(?i)(\b\d{1,2}\s*(?:\+|-|to)?\s*\d{0,2}\s*(?:years?|yrs|y/o/e|experience)?\b)",
    "Job Title": r"(?i)(?:hiring|join|looking for|we are hiring|position:|role:|opening for|engineer|developer|intern|manager|lead|senior|founding|specialist|analyst|principal|director|VP|fullstack|backend|frontend|ML engineer|data scientist|software architect|security engineer|mobile engineer|cloud engineer|SRE|machine learning scientist|AI researcher|UX designer|product manager|solutions architect|QA engineer|DevOps engineer|embedded systems engineer)\s+([\w\s\-/]+)"
}

# **🔹 Storage for Extracted Job Data**
extracted_jobs = []

# **🔹 Load JSON Data**
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# **🔹 Process Each Job Post**
for category, year_data in data.items():
    for year_month, details in sorted(year_data.items(), key=lambda x: pd.to_datetime(x[0], errors="coerce")):
        # Extract Year & Month
        match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", year_month)
        extracted_month, extracted_year = match.groups() if match else ("Unknown", "Unknown")

        for post in details.get("comments", []):  # Extract job descriptions
            extracted_info = {
                "Year": extracted_year,
                "Month": extracted_month,
                "Job Post": post[:500].strip()  # Limit job post text to 500 characters
            }

            # **🔹 Extract Details Using Patterns**
            for key, pattern in patterns.items():
                matches = re.findall(pattern, post)

                # **🔹 Handling for Different Fields**
                if key == "Salary":
                    valid_salaries = [s for s in matches if "$" in s or "K" in s or "%" in s]
                    extracted_info[key] = ", ".join(valid_salaries) if valid_salaries else "Not Specified"

                elif key == "Experience":
                    valid_experience = [s for s in matches if "year" in s.lower() or "yrs" in s.lower()]
                    extracted_info[key] = ", ".join(valid_experience) if valid_experience else "Not Specified"

                elif key == "Location":
                    location_list = [place.strip() for place in matches if len(place.strip()) > 3]
                    extracted_info[key] = ", ".join(set(location_list)) if location_list else "Not Specified"

                elif key == "Job Title":
                    extracted_info[key] = matches[0] if matches else "Not Specified"

                else:
                    extracted_info[key] = ", ".join(set(matches)) if matches else "Not Specified"

            extracted_jobs.append(extracted_info)

# **🔹 Convert Data to DataFrame & Sort**
df = pd.DataFrame(extracted_jobs)

# **Ensure Year & Month are in Order**
df["Year"] = df["Year"].astype(str)
df["Month"] = pd.Categorical(df["Month"], 
    categories=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 
    ordered=True)
df = df.sort_values(by=["Year", "Month"])

# **🔹 Save to Excel**
df.to_excel(output_file, index=False)

print(f"✅ Extracted job details saved to: {output_file}")
