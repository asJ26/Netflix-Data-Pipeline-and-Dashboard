import random
from datetime import datetime, timedelta
import csv
import json

class EnhancedNetflixSimulator:
    def __init__(self):
        self.show_id_counter = 1
        
        self.content_types = ['Movie', 'TV Show']
        self.content_weights = [0.7, 0.3]  # 70% movies, 30% TV shows
        
        self.genres = [
            'Documentaries', 'Dramas', 'Comedies', 'Action & Adventure',
            'International Movies', 'Romantic Movies', 'Horror Movies',
            'Sci-Fi & Fantasy', 'Thrillers', 'Kids\' TV', 'Anime Features',
            'Stand-Up Comedy', 'Independent Movies', 'Sports Movies',
            'Music & Musicals', 'Reality TV', 'LGBTQ Movies'
        ]
        
        self.countries = [
            'United States', 'India', 'United Kingdom', 'Japan', 'South Korea',
            'France', 'Spain', 'Germany', 'Brazil', 'Mexico', 'Canada', 
            'Australia', 'Italy', 'Nigeria', 'South Africa', 'Thailand',
            'Indonesia', 'Turkey', 'Egypt', 'Argentina', 'Netherlands'
        ]
        
        self.languages = [
            'English', 'Hindi', 'Spanish', 'French', 'Japanese', 'Korean',
            'German', 'Italian', 'Portuguese', 'Turkish', 'Arabic', 'Thai',
            'Indonesian', 'Dutch', 'Russian', 'Swedish', 'Polish'
        ]
        
        self.ratings = {
            'Movie': ['G', 'PG', 'PG-13', 'R', 'TV-MA', 'TV-14', 'TV-PG'],
            'TV Show': ['TV-Y', 'TV-Y7', 'TV-G', 'TV-PG', 'TV-14', 'TV-MA']
        }
        
        self.directors = [
            'Steven Spielberg', 'Martin Scorsese', 'Christopher Nolan',
            'Quentin Tarantino', 'Bong Joon-ho', 'Ava DuVernay',
            'Greta Gerwig', 'Spike Lee', 'Guillermo del Toro',
            'Kathryn Bigelow', 'Alfonso Cuarón', 'Ang Lee',
            'Wong Kar-wai', 'Pedro Almodóvar', 'Hayao Miyazaki'
        ]
        
        self.actors = [
            'Tom Hanks', 'Meryl Streep', 'Denzel Washington', 'Viola Davis',
            'Leonardo DiCaprio', 'Cate Blanchett', 'Morgan Freeman',
            'Jennifer Lawrence', 'Brad Pitt', 'Charlize Theron',
            'Robert De Niro', 'Emma Stone', 'Samuel L. Jackson',
            'Nicole Kidman', 'Anthony Hopkins', 'Kate Winslet'
        ]
        
        self.description_templates = [
            "In this {genre} {type}, {plot_point} leads to {consequence}.",
            "A {adjective} tale of {theme} unfolds when {plot_point}.",
            "Set in {setting}, this {genre} follows {character_desc}.",
            "When {plot_point}, {character_desc} must {action}.",
            "{character_desc} {action} in this {adjective} {genre}."
        ]
        
        self.plot_points = [
            "a mysterious disappearance", "an unexpected discovery",
            "a chance encounter", "a life-changing decision",
            "a tragic event", "a surprising revelation",
            "a daring mission", "a forbidden love",
            "a dangerous conspiracy", "an ancient secret"
        ]
        
        self.adjectives = [
            "compelling", "heartwarming", "thrilling", "provocative",
            "inspiring", "mind-bending", "emotional", "hilarious",
            "suspenseful", "thought-provoking"
        ]
        
        self.themes = [
            "love and loss", "redemption", "family bonds",
            "personal growth", "justice", "survival",
            "friendship", "betrayal", "courage", "identity"
        ]
        
        self.settings = [
            "a bustling metropolis", "a quiet suburban town",
            "a remote village", "a dystopian future",
            "a magical realm", "a war-torn country",
            "an elite university", "a mysterious island"
        ]
        
        self.character_descriptions = [
            "an ambitious young professional",
            "a determined detective",
            "a struggling artist",
            "a brilliant scientist",
            "a mysterious stranger",
            "an ordinary family",
            "a group of unlikely friends",
            "a seasoned veteran"
        ]
        
        self.actions = [
            "embark on an epic journey",
            "fight against all odds",
            "discover the truth",
            "face their deepest fears",
            "challenge the system",
            "pursue their dreams",
            "solve an impossible mystery",
            "overcome incredible obstacles"
        ]

    def generate_show_id(self):
        show_id = f"s{self.show_id_counter}"
        self.show_id_counter += 1
        return show_id

    def generate_cast(self):
        num_cast = random.randint(3, 8)
        return ", ".join(random.sample(self.actors, num_cast))

    def generate_description(self):
        template = random.choice(self.description_templates)
        return template.format(
            genre=random.choice(self.genres).lower(),
            type=random.choice(self.content_types).lower(),
            plot_point=random.choice(self.plot_points),
            consequence=random.choice(self.actions),
            adjective=random.choice(self.adjectives),
            theme=random.choice(self.themes),
            setting=random.choice(self.settings),
            character_desc=random.choice(self.character_descriptions),
            action=random.choice(self.actions)
        )

    def generate_date_added(self):
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 12, 31)
        days_between = (end_date - start_date).days
        random_days = random.randint(0, days_between)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%B %d, %Y")

    def generate_duration(self, content_type):
        if content_type == 'Movie':
            return f"{random.randint(75, 180)} min"
        else:
            return f"{random.randint(1, 8)} Seasons"

    def generate_listed_in(self):
        num_genres = random.randint(1, 3)
        return ", ".join(random.sample(self.genres, num_genres))

    def generate_entry(self):
        content_type = random.choices(self.content_types, weights=self.content_weights)[0]
        
        entry = {
            'show_id': self.generate_show_id(),
            'type': content_type,
            'title': f"Sample Title {self.show_id_counter}",  # Simplified for example
            'director': random.choice(self.directors) if random.random() > 0.2 else "",
            'cast': self.generate_cast(),
            'country': random.choice(self.countries),
            'date_added': self.generate_date_added(),
            'release_year': random.randint(2015, 2023),
            'rating': random.choice(self.ratings[content_type]),
            'duration': self.generate_duration(content_type),
            'listed_in': self.generate_listed_in(),
            'description': self.generate_description()
        }
        
        return entry

    def generate_dataset(self, num_entries=3000):
        dataset = []
        for _ in range(num_entries):
            dataset.append(self.generate_entry())
        return dataset

    def save_to_csv(self, dataset, filename='netflix_titles.csv'):
        fieldnames = ['show_id', 'type', 'title', 'director', 'cast', 'country',
                     'date_added', 'release_year', 'rating', 'duration',
                     'listed_in', 'description']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)

if __name__ == "__main__":
    simulator = EnhancedNetflixSimulator()
    dataset = simulator.generate_dataset(3000)
    simulator.save_to_csv(dataset)
    print(f"Generated 3000 entries and saved to netflix_titles.csv")
