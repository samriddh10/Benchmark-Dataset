import pandas as pd

# File paths
file1 = '/Users/sam/Desktop/Sem5/AI/myenv/movie_reviews_28OCT.csv'  # Original CSV file
file2 = '/Users/sam/Desktop/Sem5/AI/myenv/missing_movie_reviews.csv'  # CSV file to append

# Read both CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Concatenate the dataframes (append df2 to df1)
combined_data = pd.concat([df1, df2], ignore_index=True)

# Save the combined data back to the first CSV file
combined_data.to_csv(file1, index=False)

print("Data from the second file appended successfully to the first CSV file!")
