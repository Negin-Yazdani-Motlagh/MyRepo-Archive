import pandas as pd
import os

def analyze_dictionary11():
    # Get the path to the Excel file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "Dictionary of soft skills (11).xlsx")
    
    print("Loading Dictionary 11 Excel file...")
    df = pd.read_excel(excel_path)
    
    # Display basic information about the Excel file
    print("\nExcel File Structure:")
    print("====================")
    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")
    print("\nColumn names:")
    for col in df.columns:
        print(f"  - {col}")
    
    # Show unique values in each column
    print("\nUnique values in each column:")
    for col in df.columns:
        unique_values = df[col].nunique()
        print(f"\n{col}:")
        print(f"  Number of unique values: {unique_values}")
        if unique_values < 10:  # Only show values if there are few of them
            print("  Values:", df[col].unique())
    
    # Show sample data
    print("\nSample data (first 5 rows):")
    print(df.head())

if __name__ == "__main__":
    analyze_dictionary11() 
