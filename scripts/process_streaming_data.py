import json
from google.cloud import bigquery
import os
import random
from datetime import datetime, timedelta
from create_dashboard_views import create_bigquery_views

def generate_realistic_sample_data():
    """Generate realistic sample data with proper variations"""
    
    # Helper function to generate realistic timestamps
    def generate_timestamp():
        start_date = datetime(2024, 1, 1)
        days = random.randint(0, 60)  # Last 60 days
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        return (start_date + timedelta(days=days, hours=hours, minutes=minutes)).isoformat()

    # Content generation data
    genres = ["Action", "Drama", "Comedy", "Sci-Fi", "Romance", "Documentary", "Thriller", 
             "Horror", "Adventure", "Animation", "Crime", "Fantasy", "Mystery", "Family"]
    languages = ["English", "Spanish", "French", "Japanese", "Korean", "Hindi", "German", 
                "Italian", "Mandarin", "Portuguese", "Russian", "Arabic"]
    ratings = ["G", "PG", "PG-13", "R", "TV-MA", "TV-14", "TV-PG", "TV-Y7", "TV-Y"]
    
    # Generate 200 diverse content items (increased from 50)
    contents_data = []
    for i in range(200):
        genre = random.choice(genres)
        content_type = random.choice(["movie", "series"])
        duration = random.randint(25, 60) if content_type == "series" else random.randint(85, 180)
        
        content = {
            "content_id": f"content-{i+1:04d}",
            "type": content_type,
            "title": f"The {genre} {random.choice(['Adventure', 'Story', 'Tale', 'Journey', 'Experience', 'Mystery', 'Chronicles'])} {i+1}",
            "genre": genre,
            "release_year": random.randint(2020, 2024),
            "duration_minutes": duration,
            "language": random.choice(languages),
            "rating": random.choice(ratings),
            "tags": random.sample(["action", "adventure", "drama", "comedy", "romance", "thriller", 
                                 "mystery", "sci-fi", "fantasy", "documentary", "crime", "family",
                                 "animation", "horror", "musical", "biography", "sport", "history"], 3)
        }
        contents_data.append(content)

    # Generate 10000 diverse users (increased from 1000)
    countries = ["United States", "Canada", "United Kingdom", "France", "Germany", "Japan", 
                "South Korea", "Australia", "Brazil", "India", "Mexico", "Spain", "Italy", 
                "Netherlands", "Sweden", "Singapore", "UAE", "South Africa", "Argentina", "China"]
    age_groups = ["13-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    subscription_types = ["basic", "standard", "premium", "student", "family"]
    
    users_data = []
    for i in range(10000):
        # Generate realistic user preferences
        country = random.choice(countries)
        age_group = random.choice(age_groups)
        
        # Adjust subscription type probabilities based on age and country
        sub_probs = {"basic": 0.3, "standard": 0.4, "premium": 0.2, "student": 0.05, "family": 0.05}
        if age_group in ["18-24", "25-34"]:
            sub_probs["student"] = 0.15
            sub_probs["premium"] = 0.15
        elif age_group in ["35-44", "45-54"]:
            sub_probs["family"] = 0.2
            sub_probs["basic"] = 0.2
        
        subscription = random.choices(
            list(sub_probs.keys()),
            weights=list(sub_probs.values())
        )[0]
        
        # Generate language preferences based on country
        local_languages = {
            "United States": ["English", "Spanish"],
            "Canada": ["English", "French"],
            "France": ["French", "English"],
            "Germany": ["German", "English"],
            "Japan": ["Japanese", "English"],
            "South Korea": ["Korean", "English"],
            "Brazil": ["Portuguese", "English", "Spanish"],
            "India": ["Hindi", "English"],
            "China": ["Mandarin", "English"]
        }
        
        base_languages = local_languages.get(country, ["English"])
        additional_languages = random.sample([l for l in languages if l not in base_languages], 
                                          random.randint(0, 2))
        preferred_languages = base_languages + additional_languages
        
        # Generate genre preferences based on age and other factors
        genre_weights = {genre: random.random() for genre in genres}
        if age_group in ["13-17", "18-24"]:
            genre_weights["Action"] *= 1.5
            genre_weights["Sci-Fi"] *= 1.5
            genre_weights["Animation"] *= 1.3
        elif age_group in ["25-34", "35-44"]:
            genre_weights["Drama"] *= 1.4
            genre_weights["Thriller"] *= 1.3
            genre_weights["Comedy"] *= 1.3
        
        preferred_genres = random.sample(
            genres,
            k=random.randint(3, 6),
            counts=[int(genre_weights[g] * 10) for g in genres]
        )
        
        user = {
            "user_id": f"user-{i+1:04d}",
            "country": country,
            "subscription_type": subscription,
            "age_group": age_group,
            "join_date": (datetime(2024, 1, 1) - timedelta(days=random.randint(0, 730))).isoformat(),
            "preferred_genres": preferred_genres,
            "preferred_languages": preferred_languages,
            "has_profile_pin": random.choice([True, False]),
            "max_stream_quality": "4K" if subscription == "premium" else ("HD" if subscription in ["standard", "family"] else "SD")
        }
        users_data.append(user)

    # Generate 100000 viewing events (increased from 10000)
    device_types = ["smart_tv", "mobile", "tablet", "gaming_console", "desktop", "streaming_stick"]
    event_types = ["start", "pause", "resume", "complete", "exit", "seek_forward", "seek_backward"]
    connection_types = ["wifi", "ethernet", "4G", "5G", "3G"]
    playback_qualities = ["SD", "HD", "FHD", "4K"]
    algorithm_types = ["content_based", "collaborative_filtering", "hybrid", "trending", "personalized"]
    recommendation_categories = ["trending", "because_you_watched", "new_releases", "top_picks", "similar_content"]

    viewing_events_data = []
    
    for _ in range(100000):
        user = random.choice(users_data)
        
        # Select content based on user preferences
        matching_content = [c for c in contents_data 
                          if c["genre"] in user["preferred_genres"] 
                          or c["language"] in user["preferred_languages"]]
        
        content = random.choice(matching_content if matching_content else contents_data)
        
        # Device selection based on user characteristics
        if user["subscription_type"] in ["premium", "family"]:
            device_weights = [3, 1, 1, 2, 2, 2]  # Higher weight for smart_tv
        else:
            device_weights = [2, 2, 2, 1, 2, 1]  # More balanced
        
        device_type = random.choices(device_types, weights=device_weights)[0]
        
        # Connection type based on device and country
        if device_type in ["smart_tv", "desktop"]:
            conn_weights = [5, 3, 0, 1, 0]  # Prefer wifi/ethernet
        else:
            conn_weights = [3, 0, 2, 2, 1]  # More mobile connections
        
        connection = random.choices(connection_types, weights=conn_weights)[0]
        
        # Quality metrics based on connection and subscription
        if connection in ["ethernet", "5G"] and user["subscription_type"] in ["premium", "family"]:
            buffering_events = random.randint(0, 2)
            bandwidth = random.uniform(80, 200)
            frames_dropped = random.uniform(0.001, 0.005)
            startup_time = random.uniform(0.5, 2.0)
        elif connection == "4G" or user["subscription_type"] == "standard":
            buffering_events = random.randint(1, 4)
            bandwidth = random.uniform(15, 45)
            frames_dropped = random.uniform(0.002, 0.008)
            startup_time = random.uniform(1.5, 3.0)
        else:
            buffering_events = random.randint(2, 7)
            bandwidth = random.uniform(5, 15)
            frames_dropped = random.uniform(0.005, 0.015)
            startup_time = random.uniform(2.5, 4.0)

        # Generate engagement metrics based on content and user match
        base_completion = random.uniform(0.1, 1.0)
        base_engagement = random.uniform(0.1, 0.95)
        
        # Adjust engagement based on various factors
        if content["genre"] in user["preferred_genres"]:
            base_engagement *= 1.2
            base_completion *= 1.15
        if content["language"] in user["preferred_languages"]:
            base_engagement *= 1.1
            base_completion *= 1.1
        if user["subscription_type"] in ["premium", "family"]:
            base_engagement *= 1.1
        
        # Cap the metrics at 1.0
        completion_rate = min(base_completion, 1.0)
        engagement_score = min(base_engagement, 1.0)

        event = {
            "event_id": f"evt-{random.randint(100000, 999999)}",
            "timestamp": generate_timestamp(),
            "event_type": random.choice(event_types),
            "content_id": content["content_id"],
            "user_id": user["user_id"],
            "device_type": device_type,
            "watch_duration_seconds": random.randint(300, 7200),
            "session_id": f"sess-{random.randint(100000, 999999)}",
            "quality_metrics": {
                "buffering_events": buffering_events,
                "average_bitrate": random.randint(2000, 8000),
                "playback_quality": random.choice(playback_qualities),
                "connection_type": connection,
                "bandwidth_mbps": bandwidth,
                "startup_time_seconds": startup_time,
                "frames_dropped_ratio": frames_dropped,
                "audio_quality_score": random.uniform(0.8, 1.0)
            },
            "user_interaction": {
                "rewind_count": random.randint(0, 5),
                "forward_count": random.randint(0, 5),
                "pause_count": random.randint(0, 8),
                "quality_changes": random.randint(0, 3),
                "subtitle_changes": random.randint(0, 2),
                "volume_changes": random.randint(0, 5)
            },
            "recommendation_data": {
                "algorithm_type": random.choice(algorithm_types),
                "recommendation_score": random.uniform(0.1, 1.0),
                "position_in_list": random.randint(1, 20),
                "recommendation_category": random.choice(recommendation_categories)
            },
            "engagement_signals": {
                "completion_rate": completion_rate,
                "engagement_score": engagement_score,
                "social_sharing": random.choice([True, False]),
                "rating_given": random.choice([None, 1, 2, 3, 4, 5])
            }
        }
        viewing_events_data.append(event)

    return contents_data, users_data, viewing_events_data

def save_sample_data():
    """Save the sample data to JSON files"""
    # Ensure the data/raw directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate realistic sample data
    contents_data, users_data, viewing_events_data = generate_realistic_sample_data()
    
    # Save the data to files
    with open('data/raw/contents.json', 'w') as f:
        json.dump(contents_data, f, indent=2)
    
    with open('data/raw/users.json', 'w') as f:
        json.dump(users_data, f, indent=2)
    
    with open('data/raw/viewing_events.json', 'w') as f:
        json.dump(viewing_events_data, f, indent=2)
    
    print("Sample data saved to data/raw/")

def setup_bigquery():
    """Set up BigQuery tables and load data"""
    # Import and run the BigQuery setup script
    from setup_bigquery import create_dataset_and_tables, load_data_to_bigquery
    
    print("Setting up BigQuery tables...")
    create_dataset_and_tables()
    
    print("Loading data into BigQuery...")
    load_data_to_bigquery()

def create_views():
    """Create BigQuery views for data processing"""
    print("\nCreating BigQuery views for data processing...")
    create_bigquery_views()

def generate_visualizations():
    """Generate visualizations from BigQuery views"""
    # Import and run the visualization script
    from create_visualizations import main as create_viz
    
    print("Generating visualizations from BigQuery views...")
    create_viz()

def main():
    try:
        # Step 1: Generate and save sample data
        print("Step 1: Generating sample data...")
        save_sample_data()
        
        # Step 2: Set up BigQuery and load data
        print("\nStep 2: Setting up BigQuery and loading data...")
        setup_bigquery()
        
        # Step 3: Create BigQuery views for data processing
        print("\nStep 3: Creating BigQuery views...")
        create_views()
        
        # Step 4: Generate visualizations from views
        print("\nStep 4: Generating visualizations...")
        generate_visualizations()
        
        print("\nData processing and visualization complete!")
        print("All data processing was performed in BigQuery.")
        print("You can find the visualizations in the data/processed/visualizations directory")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if hasattr(e, 'errors'):
            for error in e.errors:
                print(f"Error details: {error}")

if __name__ == "__main__":
    main()
