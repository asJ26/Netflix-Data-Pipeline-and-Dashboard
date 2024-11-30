import os
import json
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def fetch_and_process_netflix_data():
    """
    Fetch Netflix shows dataset from Kaggle and process it into a format
    suitable for our simulation.
    """
    print("Fetching Netflix dataset from Kaggle...")
    
    # Create data directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/reference', exist_ok=True)
    
    try:
        # Initialize the Kaggle API
        api = KaggleApi()
        api.authenticate()
        
        # Download the dataset
        print("Downloading dataset...")
        api.dataset_download_files('shivamb/netflix-shows', path='data/raw', unzip=True)
        
        # Read the CSV file
        netflix_df = pd.read_csv('data/raw/netflix_titles.csv')
        
        print(f"Downloaded dataset with {len(netflix_df)} entries")
        
        # Process the data
        processed_content = []
        
        for _, row in netflix_df.iterrows():
            # Extract genres and cast
            genres = row['listed_in'].split(', ') if pd.notna(row['listed_in']) else []
            cast = row['cast'].split(', ') if pd.notna(row['cast']) else []
            
            # Extract duration and convert to minutes
            duration = 0
            duration_str = str(row['duration']) if pd.notna(row['duration']) else ''
            if 'Season' in duration_str or 'Seasons' in duration_str:
                # For TV shows, estimate ~10 episodes per season, ~45 minutes per episode
                num_seasons = int(duration_str.split()[0])
                duration = num_seasons * 10 * 45
            elif 'min' in duration_str:
                duration = int(duration_str.split()[0])
            
            # Create content entry
            content = {
                'show_id': row['show_id'],
                'type': row['type'],
                'title': row['title'],
                'director': row['director'] if pd.notna(row['director']) else None,
                'cast': cast,
                'country': row['country'] if pd.notna(row['country']) else None,
                'date_added': row['date_added'] if pd.notna(row['date_added']) else None,
                'release_year': int(row['release_year']) if pd.notna(row['release_year']) else None,
                'rating': row['rating'] if pd.notna(row['rating']) else None,
                'duration_minutes': duration,
                'genres': genres,
                'description': row['description'] if pd.notna(row['description']) else None
            }
            
            processed_content.append(content)
        
        # Save processed data
        with open('data/reference/netflix_content.json', 'w') as f:
            json.dump(processed_content, f, indent=2)
        
        # Save some useful reference data
        reference_data = {
            'genres': list(set([genre for content in processed_content 
                              for genre in content['genres']])),
            'ratings': list(set([content['rating'] for content in processed_content 
                               if content['rating'] is not None])),
            'countries': list(set([content['country'] for content in processed_content 
                                 if content['country'] is not None])),
            'content_types': list(set([content['type'] for content in processed_content])),
            'release_years': list(set([content['release_year'] for content in processed_content 
                                     if content['release_year'] is not None]))
        }
        
        with open('data/reference/reference_data.json', 'w') as f:
            json.dump(reference_data, f, indent=2)
        
        print(f"\nProcessed {len(processed_content)} content items")
        print("\nContent statistics:")
        print(f"Movies: {sum(1 for c in processed_content if c['type'] == 'Movie')}")
        print(f"TV Shows: {sum(1 for c in processed_content if c['type'] == 'TV Show')}")
        print(f"Unique genres: {len(reference_data['genres'])}")
        print(f"Year range: {min(reference_data['release_years'])} - {max(reference_data['release_years'])}")
        
        print("\nFiles saved:")
        print("- data/reference/netflix_content.json")
        print("- data/reference/reference_data.json")
        
        return processed_content, reference_data
        
    except Exception as e:
        print(f"Error fetching or processing Netflix data: {e}")
        print("\nTo use the Kaggle API, please follow these steps:")
        print("1. Sign up for a Kaggle account at https://www.kaggle.com")
        print("2. Go to your account settings (https://www.kaggle.com/account)")
        print("3. Scroll to 'API' section and click 'Create New API Token'")
        print("4. This will download 'kaggle.json' file")
        print("5. Create a .kaggle directory in your home folder:")
        print("   mkdir ~/.kaggle")
        print("6. Move the downloaded kaggle.json to the .kaggle directory:")
        print("   mv path/to/kaggle.json ~/.kaggle/")
        print("7. Ensure the API token file has restricted permissions:")
        print("   chmod 600 ~/.kaggle/kaggle.json")
        print("\nAfter completing these steps, run this script again.")
        raise

if __name__ == "__main__":
    fetch_and_process_netflix_data()
