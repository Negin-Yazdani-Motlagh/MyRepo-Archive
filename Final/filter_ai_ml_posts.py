import json
import re
import os
from tqdm import tqdm

def contains_terms(text):
    """Check if text contains any of the specified terms"""
    text_lower = text.lower()
    
    # All terms to look for
    terms = {
        'AI': r'\bai\b',
        'Artificial Intelligence': 'artificial intelligence',
        'ML': r'\bml\b',
        'Machine Learning': 'machine learning',
        'LLM': r'\bllm\b',
        'Natural Language Processing': 'natural language processing'
    }
    
    found_terms = {}
    for term, pattern in terms.items():
        if re.search(pattern, text_lower):
            found_terms[term] = True
    
    return found_terms

def filter_ai_ml_posts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_path = os.path.join(script_dir, "JSON", "Yearly_Job_Posts.json")
    output_json_path = os.path.join(script_dir, "JSON", "AI_ML_Job_Posts.json")
    
    print("Loading JSON file...")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    ai_ml_posts = {"YC": {}}
    yearly_stats = {}
    
    print("\nFiltering posts...")
    for year in tqdm(data['YC'].keys()):
        ai_ml_posts['YC'][year] = {"comments": []}
        yearly_stats[year] = {
            'total': 0,
            'ai_ml': 0,
            'term_counts': {
                'AI': 0,
                'Artificial Intelligence': 0,
                'ML': 0,
                'Machine Learning': 0,
                'LLM': 0,
                'Natural Language Processing': 0
            }
        }
        
        for comment in data['YC'][year]['comments']:
            yearly_stats[year]['total'] += 1
            found_terms = contains_terms(comment)
            
            if found_terms:
                ai_ml_posts['YC'][year]['comments'].append(comment)
                yearly_stats[year]['ai_ml'] += 1
                
                # Count individual terms
                for term in found_terms:
                    yearly_stats[year]['term_counts'][term] += 1
    
    # Save filtered data
    print("\nSaving filtered data...")
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(ai_ml_posts, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    print("\nYearly Statistics:")
    print("================")
    for year in sorted(yearly_stats.keys()):
        stats = yearly_stats[year]
        percentage = (stats['ai_ml'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"\nYear {year}:")
        print(f"  Total posts: {stats['total']}")
        print(f"  AI/ML posts: {stats['ai_ml']}")
        print(f"  Percentage: {percentage:.2f}%")
        print("  Term breakdown:")
        for term, count in stats['term_counts'].items():
            print(f"    - {term}: {count}")
    
    # Validate trend after 2022
    years_after_2022 = [int(y) for y in yearly_stats.keys() if int(y) >= 2022]
    years_after_2022.sort()
    
    if len(years_after_2022) > 1:
        print("\nTrend Validation (2022 onwards):")
        print("==============================")
        prev_percentage = None
        for year in years_after_2022:
            stats = yearly_stats[str(year)]
            current_percentage = (stats['ai_ml'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
            if prev_percentage is not None:
                if current_percentage < prev_percentage:
                    print(f"WARNING: Decrease detected from {year-1} ({prev_percentage:.2f}%) to {year} ({current_percentage:.2f}%)")
            prev_percentage = current_percentage
    
    print(f"\nFiltered data saved to: {output_json_path}")

if __name__ == "__main__":
    filter_ai_ml_posts() 
