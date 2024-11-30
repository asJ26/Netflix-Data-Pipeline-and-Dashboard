from google.cloud import bigquery
from datetime import datetime

def run_analysis():
    client = bigquery.Client()
    
    # Dictionary to store our queries
    queries = {
        'top_content': """
            SELECT 
                c.title,
                c.genre,
                COUNT(DISTINCT v.user_id) as unique_viewers,
                SUM(v.watch_duration_seconds)/3600 as total_watch_hours,
                AVG(v.watch_duration_seconds)/60 as avg_watch_minutes
            FROM `netflix_analytics.viewing_events` v
            JOIN `netflix_analytics.contents` c ON v.content_id = c.content_id
            GROUP BY c.title, c.genre
            ORDER BY unique_viewers DESC
            LIMIT 10
        """,
        
        'device_distribution': """
            SELECT 
                device_type,
                COUNT(*) as session_count,
                COUNT(DISTINCT user_id) as unique_users,
                AVG(watch_duration_seconds)/60 as avg_session_minutes
            FROM `netflix_analytics.viewing_events`
            GROUP BY device_type
            ORDER BY session_count DESC
        """,
        
        'quality_metrics': """
            SELECT 
                c.title,
                AVG(v.quality_metrics.buffering_events) as avg_buffering_events,
                AVG(v.quality_metrics.average_bitrate) as avg_bitrate,
                COUNT(CASE WHEN v.quality_metrics.playback_quality = '4K' THEN 1 END) as total_4k_plays,
                COUNT(*) as total_plays
            FROM `netflix_analytics.viewing_events` v
            JOIN `netflix_analytics.contents` c ON v.content_id = c.content_id
            GROUP BY c.title
            HAVING total_plays > 5
            ORDER BY avg_buffering_events ASC
            LIMIT 10
        """,
        
        'user_engagement': """
            SELECT 
                u.subscription_type,
                u.age_group,
                COUNT(DISTINCT u.user_id) as user_count,
                COUNT(*) as total_sessions,
                AVG(v.watch_duration_seconds)/60 as avg_session_minutes,
                COUNT(*)/COUNT(DISTINCT u.user_id) as sessions_per_user
            FROM `netflix_analytics.users` u
            JOIN `netflix_analytics.viewing_events` v ON u.user_id = v.user_id
            GROUP BY u.subscription_type, u.age_group
            ORDER BY user_count DESC
        """
    }
    
    # Run each query and print results
    for analysis_name, query in queries.items():
        print(f"\n=== {analysis_name.replace('_', ' ').title()} Analysis ===")
        try:
            query_job = client.query(query)
            results = query_job.result()
            
            # Print column headers
            headers = [field.name for field in results.schema]
            header_row = " | ".join(f"{header:20}" for header in headers)
            print("\n" + header_row)
            print("-" * len(header_row))
            
            # Print results
            for row in results:
                row_values = [str(value) if value is not None else "NULL" for value in row.values()]
                print(" | ".join(f"{value:20}" for value in row_values))
                
        except Exception as e:
            print(f"Error running {analysis_name} analysis: {e}")

if __name__ == "__main__":
    print("Running Netflix content performance analysis...")
    run_analysis()
