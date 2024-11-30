import json
import random
from datetime import datetime, timedelta
import uuid

class NetflixDataSimulator:
    def __init__(self):
        self.content_types = ['movie', 'series']
        self.genres = ['action', 'comedy', 'drama', 'documentary', 'thriller', 'romance', 'sci-fi', 'horror', 'family', 'anime']
        self.devices = ['smart_tv', 'mobile', 'tablet', 'laptop', 'desktop', 'gaming_console', 'streaming_stick']
        self.event_types = ['start', 'pause', 'resume', 'complete', 'exit']
        self.countries = ['US', 'UK', 'CA', 'AU', 'FR', 'DE', 'JP', 'BR', 'IN', 'MX', 'ES', 'IT', 'NL', 'SG', 'KR']
        self.series_episodes = {}  # To track episodes for series

    def generate_content(self):
        content_type = random.choice(self.content_types)
        content_id = str(uuid.uuid4())
        
        if content_type == 'series':
            num_episodes = random.randint(8, 24)
            self.series_episodes[content_id] = num_episodes
            episode_duration = random.randint(25, 60)
        else:
            episode_duration = random.randint(90, 180)

        return {
            'content_id': content_id,
            'type': content_type,
            'title': f"Sample {content_type.title()} {random.randint(1, 1000)}",
            'genre': random.choice(self.genres),
            'release_year': random.randint(2018, 2024),
            'duration_minutes': episode_duration,
            'language': random.choice(['English', 'Spanish', 'French', 'Japanese', 'Korean', 'Hindi']),
            'rating': random.choice(['G', 'PG', 'PG-13', 'R', 'TV-MA', 'TV-14', 'TV-PG']),
            'tags': random.sample(['action-packed', 'emotional', 'suspenseful', 'thought-provoking', 
                                 'romantic', 'dark', 'funny', 'classic', 'award-winning'], 3)
        }

    def generate_user(self, user_id):
        join_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        return {
            'user_id': user_id,
            'country': random.choice(self.countries),
            'subscription_type': random.choice(['basic', 'standard', 'premium']),
            'age_group': random.choice(['18-24', '25-34', '35-44', '45-54', '55+']),
            'join_date': join_date.isoformat(),
            'preferred_genres': random.sample(self.genres, random.randint(2, 4)),
            'preferred_languages': random.sample(['English', 'Spanish', 'French', 'Japanese', 'Korean', 'Hindi'], 
                                              random.randint(1, 3)),
            'has_profile_pin': random.choice([True, False]),
            'max_stream_quality': random.choice(['HD', '4K', 'SD'])
        }

    def generate_viewing_event(self, content, user, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
        
        event_type = random.choice(self.event_types)
        max_duration = content['duration_minutes'] * 60  # Convert to seconds
        
        if event_type == 'complete':
            watch_duration = max_duration
        elif event_type == 'exit':
            watch_duration = random.randint(1, max_duration)
        else:
            watch_duration = random.randint(max_duration // 4, max_duration)

        quality_issues = random.random() < 0.15  # 15% chance of quality issues
        
        return {
            'event_id': str(uuid.uuid4()),
            'timestamp': timestamp.isoformat(),
            'event_type': event_type,
            'content_id': content['content_id'],
            'user_id': user['user_id'],
            'device_type': random.choice(self.devices),
            'watch_duration_seconds': watch_duration,
            'quality_metrics': {
                'buffering_events': random.randint(3, 8) if quality_issues else random.randint(0, 2),
                'average_bitrate': random.randint(2000, 8000),
                'playback_quality': random.choice(['SD', 'HD', '4K']),
                'connection_type': random.choice(['wifi', '4G', '5G', 'ethernet']),
                'startup_time_seconds': random.uniform(0.5, 3.0),
                'frames_dropped_ratio': random.uniform(0, 0.02) if quality_issues else random.uniform(0, 0.005)
            },
            'user_interaction': {
                'rewind_count': random.randint(0, 3),
                'forward_count': random.randint(0, 3),
                'pause_count': random.randint(0, 5)
            }
        }

    def generate_batch_events(self, num_users=500, events_per_user_range=(15, 40)):
        print("Generating sample Netflix viewing data...")
        
        # Generate content items (mix of movies and series)
        contents = [self.generate_content() for _ in range(200)]  # 200 unique content items
        print(f"Generated {len(contents)} unique content items")

        # Generate users
        users = []
        for i in range(num_users):
            user_id = str(uuid.uuid4())
            users.append(self.generate_user(user_id))
        print(f"Generated {len(users)} unique users")

        # Generate viewing events
        events = []
        total_events = 0
        
        for user in users:
            # Each user watches between 15-40 pieces of content
            num_events = random.randint(*events_per_user_range)
            user_contents = random.sample(contents, num_events)
            
            for content in user_contents:
                # Generate 1-3 viewing sessions for each content
                num_sessions = random.randint(1, 3)
                for _ in range(num_sessions):
                    timestamp = datetime.now() - timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                    event = self.generate_viewing_event(content, user, timestamp)
                    events.append(event)
                    total_events += 1

        print(f"Generated {total_events} viewing events")
        
        return {
            'contents': contents,
            'users': users,
            'events': events
        }

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    simulator = NetflixDataSimulator()
    
    # Generate sample data with 500 users
    data = simulator.generate_batch_events(500)
    
    # Save to different files for better organization
    save_to_json(data['contents'], 'data/raw/contents.json')
    save_to_json(data['users'], 'data/raw/users.json')
    save_to_json(data['events'], 'data/raw/viewing_events.json')
    
    print(f"\nFiles saved in data/raw/ directory:")
    print(f"- {len(data['contents'])} unique content items")
    print(f"- {len(data['users'])} unique users")
    print(f"- {len(data['events'])} viewing events")
