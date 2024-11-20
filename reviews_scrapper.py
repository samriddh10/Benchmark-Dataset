import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os

# Setup logging
logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to clean text by removing illegal characters
def clean_text(text):
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

# Function to extract reviews from IMDb
def get_reviews(movie_id):
    url = f'https://www.imdb.com/title/{movie_id}/reviews'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching reviews for {movie_id}: {e}")
        return []

    # Parse reviews using the updated class name
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = [clean_text(review.get_text(strip=True)) 
               for review in soup.find_all('div', class_='ipc-html-content-inner-div')[:10]]
    
    return reviews

# Load movie IDs from Excel file
input_file = "/Users/sam/Desktop/Sem5/AI/myenv/missing_reviews.xlsx"
movies_df = pd.read_excel(input_file)

# Output file for saving reviews
output_file = '/Users/sam/Desktop/Sem5/AI/myenv/missing_movie_reviews.csv'

# Create CSV file with headers if it doesn't exist
if not os.path.exists(output_file):
    pd.DataFrame(columns=['Movie ID', 'Movie Name', 'Review']).to_csv(output_file, index=False)

# Collect and save reviews for each movie in the Excel file
for index, row in movies_df.iterrows():
    movie_id = row['imdbid']
    movie_name = row.get('title', 'Unknown')
    print(f"Fetching reviews for {movie_name} (ID: {movie_id})...")

    reviews = get_reviews(movie_id)
    batch_data = []

    if reviews:
        for review in reviews:
            batch_data.append({'Movie ID': movie_id, 'Movie Name': movie_name, 'Review': review})

        # Append reviews for the current movie to the CSV file
        pd.DataFrame(batch_data).to_csv(output_file, mode='a', index=False, header=False)
        print(f"Reviews for {movie_name} have been successfully saved to {output_file}.")
    else:
        print(f"No reviews found for {movie_name} (ID: {movie_id}).")

print("All reviews have been successfully saved in missing_movie_reviews.csv.")
