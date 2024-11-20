import pandas as pd

# Load the Excel file and the CSV file
file1 = '/Users/sam/Desktop/Sem5/AI/myenv/modified_file_1.xlsx'
file2 = '/Users/sam/Desktop/Sem5/AI/myenv/movie_reviews_28OCT.csv'

# Read file1 (Excel) and file2 (CSV) into pandas DataFrames
df1 = pd.read_excel(file1)
df2 = pd.read_csv(file2)

# Rename columns to have a common name for comparison
df1.rename(columns={'imdbId': 'imdbid'}, inplace=True)
df2.rename(columns={'Movie ID': 'imdbid'}, inplace=True)

# Find rows in df1 where 'imdbid' does not have a match in df2
missing_reviews = df1[~df1['imdbid'].isin(df2['imdbid'])]

# Save missing "imdbId" rows to a new Excel file
missing_reviews.to_excel('/Users/sam/Desktop/Sem5/AI/myenv/missing_reviews.xlsx', index=False)

print("Rows with missing reviews have been saved to 'missing_reviews.xlsx'.")
