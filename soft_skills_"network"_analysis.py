 1. import json
 2. import re
 3.  
 4. # File paths
 5. job_posts_file = r'C:\\Users\\negin\\Neginn\\AI&Education\\nested_Job_Posts.json'
 6. output_file_sentences_json = r'C:\\Users\\negin\\Neginn\\AI&Education\\network_sentences.json'
 7.  
 8. # Helper function to extract descriptions
 9. def extract_descriptions(data):
10.     descriptions = []
11.     if isinstance(data, dict):
12.         for key, value in data.items():
13.             descriptions.extend(extract_descriptions(value))
14.     elif isinstance(data, list):
15.         for item in data:
16.             descriptions.extend(extract_descriptions(item))
17.     elif isinstance(data, str):
18.         descriptions.append(data)
19.     return descriptions
20.  
21. # Helper function to extract sentences containing the word "network"
22. def extract_sentences_with_network(description):
23.     # Split text into sentences based on common sentence delimiters
24.     sentences = re.split(r'(?<=[.!?])\s+', description)
25.     return [sentence.strip() for sentence in sentences if "network" in sentence.lower()]
26.  
27. # Main execution
28. try:
29.     # Load job post data
30.     with open(job_posts_file, 'r', encoding='utf-8') as file:
31.         job_data = json.load(file)
32.  
33.     # Extract descriptions from the nested JSON
34.     descriptions = extract_descriptions(job_data)
35.  
36.     # Extract full sentences containing "network"
37.     network_sentences = {}
38.     for index, desc in enumerate(descriptions):
39.         sentences_with_network = extract_sentences_with_network(desc.lower())
40.         if sentences_with_network:
41.             network_sentences[f"Job_Post_{index+1}"] = sentences_with_network
42.  
43.     # Save all "network" sentences to a JSON file
44.     with open(output_file_sentences_json, 'w', encoding='utf-8') as file:
45.         json.dump(network_sentences, file, indent=4)
46.  
47.     print(f"Extracted sentences containing 'network' saved in JSON format to {output_file_sentences_json}.")
48.  
49. except FileNotFoundError as e:
50.     print(f"Error: {e}")
51. except json.JSONDecodeError as e:
52.     print(f"Error decoding JSON: {e}")
53.  
