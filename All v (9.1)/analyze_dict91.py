import pandas as pd
import os
import json
from tqdm import tqdm
try:
    import cudf
    import cupy as cp
    USE_GPU = True
    print("GPU acceleration enabled")
except ImportError:
    USE_GPU = False
    print("GPU acceleration not available, using CPU")

def load_and_analyze_excel():
    # Get file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "Dictionary of soft skills (9.1).xlsx")
    
    print("\nLoading Excel file...")
    df = pd.read_excel(excel_path)
    
    if USE_GPU:
        # Convert to cuDF DataFrame
        df_gpu = cudf.DataFrame.from_pandas(df)
        
        # Basic analysis
        print("\nDataset Statistics (GPU-accelerated):")
        print("====================================")
        print(f"Total categories: {len(df_gpu['Headcategory'].unique())}")
        print(f"Total subcategories: {len(df_gpu['Subcategory'].unique())}")
        
        # Count skills per category
        category_counts = df_gpu.groupby('Headcategory').size().sort_values(ascending=False)
        
        print("\nSkills per Category:")
        print("===================")
        for category, count in category_counts.items():
            print(f"{category}: {count} skills")
            
        # Get unique categories
        categories = df_gpu['Headcategory'].unique().to_array()
        
        print("\nDetailed Category Analysis:")
        print("==========================")
        for category in categories:
            subcats = df_gpu[df_gpu['Headcategory'] == category]['Subcategory']
            print(f"\n{category}:")
            print("-" * len(category))
            for subcat in subcats:
                print(f"  - {subcat}")
    else:
        # CPU fallback analysis
        print("\nDataset Statistics:")
        print("==================")
        print(f"Total categories: {len(df['Headcategory'].unique())}")
        print(f"Total subcategories: {len(df['Subcategory'].unique())}")
        
        # Count skills per category
        category_counts = df.groupby('Headcategory').size().sort_values(ascending=False)
        
        print("\nSkills per Category:")
        print("===================")
        for category, count in category_counts.items():
            print(f"{category}: {count} skills")
            
        # Get unique categories
        categories = df['Headcategory'].unique()
        
        print("\nDetailed Category Analysis:")
        print("==========================")
        for category in categories:
            subcats = df[df['Headcategory'] == category]['Subcategory']
            print(f"\n{category}:")
            print("-" * len(category))
            for subcat in subcats:
                print(f"  - {subcat}")

if __name__ == "__main__":
    load_and_analyze_excel() 
