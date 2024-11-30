import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

class NetflixAdvancedAnalytics:
    def __init__(self):
        self.raw_data = {}
        self.processed_data = {}
        self.insights = {}
        
    def load_data(self):
        """Load raw data from JSON files"""
        data_files = {
            'contents': 'data/raw/contents.json',
            'users': 'data/raw/users.json',
            'events': 'data/raw/viewing_events.json'
        }
        
        for key, filepath in data_files.items():
            with open(filepath, 'r') as f:
                self.raw_data[key] = json.load(f)
        
        # Convert to pandas DataFrames
        self.df_contents = pd.json_normalize(self.raw_data['contents'])
        self.df_users = pd.json_normalize(self.raw_data['users'])
        self.df_events = pd.json_normalize(self.raw_data['events'])
        
        print("Data loaded successfully")
        print(f"Contents shape: {self.df_contents.shape}")
        print(f"Users shape: {self.df_users.shape}")
        print(f"Events shape: {self.df_events.shape}")

    def analyze_content_performance(self):
        """Analyze content performance metrics"""
        print("Analyzing content performance metrics...")
        
        # Merge events with content data
        events_with_content = pd.merge(
            self.df_events,
            self.df_contents[['content_id', 'type', 'genre', 'production_cost', 'marketing_budget']],
            on='content_id'
        )
        
        # Calculate basic metrics
        agg_dict = {
            'event_id': 'count',
            'watch_duration_seconds': ['sum', 'mean'],
            'quality_metrics.buffering_events': 'mean',
            'engagement_signals.completion_rate': 'mean',
            'engagement_signals.engagement_score': 'mean',
            'production_cost': 'first',
            'marketing_budget': 'first'
        }
        
        content_performance = events_with_content.groupby('content_id').agg(agg_dict)
        
        # Flatten column names
        content_performance.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in content_performance.columns]
        content_performance = content_performance.reset_index()
        
        # Calculate ROI metrics
        content_performance['total_watch_hours'] = content_performance['watch_duration_seconds_sum'] / 3600
        content_performance['cost_per_hour'] = content_performance['production_cost_first'] / content_performance['total_watch_hours']
        
        self.processed_data['content_performance'] = content_performance
        
        # Generate insights
        top_performing = content_performance.nlargest(10, 'engagement_signals.engagement_score_mean')
        cost_effective = content_performance.nsmallest(10, 'cost_per_hour')
        
        self.insights['content_performance'] = {
            'top_performing_content': top_performing.to_dict('records'),
            'cost_effective_content': cost_effective.to_dict('records')
        }

    def analyze_user_behavior(self):
        """Analyze user behavior patterns"""
        print("Analyzing user behavior patterns...")
        
        # Prepare user viewing patterns
        agg_dict = {
            'event_id': 'count',
            'watch_duration_seconds': ['sum', 'mean'],
            'quality_metrics.buffering_events': 'mean',
            'engagement_signals.engagement_score': 'mean'
        }
        
        user_viewing = self.df_events.groupby('user_id').agg(agg_dict)
        
        # Flatten column names
        user_viewing.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in user_viewing.columns]
        user_viewing = user_viewing.reset_index()
        
        # Prepare data for clustering
        clustering_features = ['watch_duration_seconds_mean', 'engagement_signals.engagement_score_mean']
        X = user_viewing[clustering_features].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform user segmentation
        kmeans = KMeans(n_clusters=5, random_state=42)
        user_viewing['user_segment'] = kmeans.fit_predict(X_scaled)
        
        self.processed_data['user_behavior'] = user_viewing
        
        # Generate insights
        segment_profiles = user_viewing.groupby('user_segment').agg({
            'user_id': 'count',
            'watch_duration_seconds_mean': 'mean',
            'engagement_signals.engagement_score_mean': 'mean'
        }).reset_index()
        
        self.insights['user_behavior'] = {
            'user_segments': segment_profiles.to_dict('records'),
            'viewing_patterns': self.analyze_viewing_patterns()
        }

    def analyze_viewing_patterns(self):
        """Analyze temporal viewing patterns"""
        self.df_events['timestamp'] = pd.to_datetime(self.df_events['timestamp'])
        self.df_events['hour'] = self.df_events['timestamp'].dt.hour
        self.df_events['day_of_week'] = self.df_events['timestamp'].dt.day_name()
        
        hourly_patterns = self.df_events.groupby('hour').size().to_dict()
        daily_patterns = self.df_events.groupby('day_of_week').size().to_dict()
        
        return {
            'hourly_patterns': hourly_patterns,
            'daily_patterns': daily_patterns
        }

    def analyze_quality_metrics(self):
        """Analyze streaming quality and technical performance"""
        print("Analyzing quality metrics...")
        
        quality_metrics = self.df_events.groupby('device_type').agg({
            'quality_metrics.buffering_events': 'mean',
            'quality_metrics.average_bitrate': 'mean',
            'quality_metrics.startup_time_seconds': 'mean',
            'quality_metrics.frames_dropped_ratio': 'mean'
        }).reset_index()
        
        # Calculate quality score per device
        quality_metrics['quality_score'] = (
            (1 - quality_metrics['quality_metrics.frames_dropped_ratio']) * 0.3 +
            (1 - quality_metrics['quality_metrics.startup_time_seconds'] / quality_metrics['quality_metrics.startup_time_seconds'].max()) * 0.3 +
            (quality_metrics['quality_metrics.average_bitrate'] / quality_metrics['quality_metrics.average_bitrate'].max()) * 0.4
        )
        
        self.processed_data['quality_metrics'] = quality_metrics
        self.insights['quality_metrics'] = {
            'device_performance': quality_metrics.to_dict('records')
        }

    def generate_visualizations(self):
        """Generate visualization plots"""
        print("Generating visualizations...")
        os.makedirs('data/processed/visualizations', exist_ok=True)
        
        # Content Performance Plot
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=self.processed_data['content_performance'], 
                       x='production_cost_first', 
                       y='engagement_signals.engagement_score_mean')
        plt.title('Content Cost vs Engagement')
        plt.xlabel('Production Cost')
        plt.ylabel('Engagement Score')
        plt.savefig('data/processed/visualizations/content_performance.png')
        plt.close()
        
        # User Segments Plot
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.processed_data['user_behavior'], 
                   x='user_segment', 
                   y='watch_duration_seconds_mean')
        plt.title('Watch Duration by User Segment')
        plt.savefig('data/processed/visualizations/user_segments.png')
        plt.close()
        
        # Quality Metrics Plot
        plt.figure(figsize=(12, 6))
        sns.barplot(data=self.processed_data['quality_metrics'],
                   x='device_type',
                   y='quality_score')
        plt.title('Quality Score by Device Type')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('data/processed/visualizations/quality_metrics.png')
        plt.close()

    def save_processed_data(self):
        """Save processed data and insights"""
        print("Saving processed data and insights...")
        os.makedirs('data/processed', exist_ok=True)
        
        # Save processed DataFrames
        for key, df in self.processed_data.items():
            df.to_csv(f'data/processed/{key}.csv', index=False)
        
        # Save insights
        with open('data/processed/insights.json', 'w') as f:
            json.dump(self.insights, f, indent=2, default=str)
        
        print("Processed data and insights saved successfully")

    def run_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting advanced analytics pipeline...")
        
        self.load_data()
        self.analyze_content_performance()
        self.analyze_user_behavior()
        self.analyze_quality_metrics()
        self.generate_visualizations()
        self.save_processed_data()
        
        print("\nAnalysis complete! Check the 'data/processed' directory for results.")
        print("\nGenerated files:")
        print("- data/processed/content_performance.csv")
        print("- data/processed/user_behavior.csv")
        print("- data/processed/quality_metrics.csv")
        print("- data/processed/insights.json")
        print("- data/processed/visualizations/content_performance.png")
        print("- data/processed/visualizations/user_segments.png")
        print("- data/processed/visualizations/quality_metrics.png")

if __name__ == "__main__":
    analyzer = NetflixAdvancedAnalytics()
    analyzer.run_analysis()
