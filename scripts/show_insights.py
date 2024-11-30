import json
import pandas as pd
from tabulate import tabulate
import os

def load_processed_data():
    """Load and display insights from processed data"""
    print("\n=== Netflix Content Analytics Insights ===\n")
    
    # Load insights.json
    with open('data/processed/insights.json', 'r') as f:
        insights = json.load(f)
    
    # Load processed CSV files
    content_perf = pd.read_csv('data/processed/content_performance.csv')
    user_behavior = pd.read_csv('data/processed/user_behavior.csv')
    quality_metrics = pd.read_csv('data/processed/quality_metrics.csv')
    
    # Display Content Performance Insights
    print("\n1. Content Performance Analysis")
    print("-" * 80)
    
    print("\nTop 5 Most Engaging Content:")
    top_content = content_perf.nlargest(5, 'engagement_signals.engagement_score_mean')[
        ['content_id', 'total_watch_hours', 'engagement_signals.engagement_score_mean', 'cost_per_hour']
    ]
    top_content.columns = ['Content ID', 'Watch Hours', 'Engagement Score', 'Cost per Hour']
    print(tabulate(top_content, headers='keys', tablefmt='grid', floatfmt='.2f'))
    
    # Display User Behavior Insights
    print("\n2. User Behavior Analysis")
    print("-" * 80)
    
    print("\nUser Segments Overview:")
    segments = user_behavior.groupby('user_segment').agg({
        'user_id': 'count',
        'watch_duration_seconds_mean': 'mean',
        'engagement_signals.engagement_score_mean': 'mean'
    }).round(2)
    segments.columns = ['User Count', 'Avg Watch Duration (s)', 'Avg Engagement Score']
    print(tabulate(segments, headers='keys', tablefmt='grid'))
    
    # Display Viewing Patterns
    print("\n3. Viewing Patterns")
    print("-" * 80)
    
    patterns = insights['user_behavior']['viewing_patterns']
    print("\nDaily Distribution:")
    daily = pd.Series(patterns['daily_patterns']).sort_values(ascending=False)
    print(tabulate(daily.reset_index(), headers=['Day', 'View Count'], tablefmt='grid'))
    
    # Display Quality Metrics
    print("\n4. Streaming Quality Analysis")
    print("-" * 80)
    
    print("\nDevice Performance Metrics:")
    quality = quality_metrics.sort_values('quality_score', ascending=False)
    quality_display = quality[['device_type', 'quality_score', 'quality_metrics.buffering_events']]
    quality_display.columns = ['Device Type', 'Quality Score', 'Avg Buffering Events']
    print(tabulate(quality_display, headers='keys', tablefmt='grid', floatfmt='.3f'))
    
    # Display ROI Analysis
    print("\n5. ROI Analysis")
    print("-" * 80)
    
    print("\nOverall Metrics:")
    overall_metrics = {
        'Total Watch Hours': content_perf['total_watch_hours'].sum(),
        'Average Engagement Score': content_perf['engagement_signals.engagement_score_mean'].mean(),
        'Average Cost per Hour': content_perf['cost_per_hour'].mean(),
        'Total Events': content_perf['event_id_count'].sum()
    }
    metrics_df = pd.DataFrame([overall_metrics]).round(2)
    print(tabulate(metrics_df.T, headers=['Metric', 'Value'], tablefmt='grid'))
    
    # Display visualization locations
    print("\n6. Generated Visualizations")
    print("-" * 80)
    print("\nVisualization files have been generated at:")
    for viz in os.listdir('data/processed/visualizations'):
        print(f"- data/processed/visualizations/{viz}")
    
    # Display data locations
    print("\n7. Processed Data Files")
    print("-" * 80)
    print("\nDetailed data available in:")
    print("- data/processed/content_performance.csv")
    print("- data/processed/user_behavior.csv")
    print("- data/processed/quality_metrics.csv")
    print("- data/processed/insights.json")

if __name__ == "__main__":
    try:
        load_processed_data()
    except FileNotFoundError as e:
        print("Error: Processed data files not found. Please run the analysis first:")
        print("python scripts/enhanced_data_simulator.py && python scripts/advanced_analytics.py")
    except Exception as e:
        print(f"Error displaying insights: {e}")
        import traceback
        traceback.print_exc()
