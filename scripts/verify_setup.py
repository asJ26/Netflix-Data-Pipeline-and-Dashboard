from google.cloud import bigquery
from tabulate import tabulate
import sys

def run_verification_queries():
    client = bigquery.Client()
    
    verification_queries = {
        "Content Overview": """
            SELECT 
                COUNT(DISTINCT content_id) as total_content,
                COUNT(DISTINCT CASE WHEN type = 'movie' THEN content_id END) as movies,
                COUNT(DISTINCT CASE WHEN type = 'series' THEN content_id END) as series,
                COUNT(DISTINCT genre) as unique_genres
            FROM netflix_analytics.content_performance_metrics
        """,
        
        "Top 5 Content by Watch Time": """
            SELECT 
                title,
                type,
                genre,
                ROUND(total_watch_hours, 2) as watch_hours,
                unique_viewers,
                ROUND(avg_watch_minutes, 2) as avg_minutes_per_view
            FROM netflix_analytics.content_performance_metrics
            ORDER BY total_watch_hours DESC
            LIMIT 5
        """,
        
        "User Engagement Summary": """
            SELECT 
                subscription_type,
                COUNT(DISTINCT user_id) as users,
                ROUND(AVG(total_watch_hours), 2) as avg_watch_hours,
                ROUND(AVG(total_sessions), 2) as avg_sessions
            FROM netflix_analytics.user_engagement_metrics
            GROUP BY subscription_type
            ORDER BY users DESC
        """,
        
        "Device Usage": """
            SELECT 
                device_type,
                COUNT(*) as total_sessions,
                ROUND(AVG(avg_session_minutes), 2) as avg_session_minutes,
                ROUND(AVG(avg_buffering_events), 2) as avg_buffering_events
            FROM netflix_analytics.device_performance_metrics
            GROUP BY device_type
            ORDER BY total_sessions DESC
        """,
        
        "Genre Performance": """
            SELECT 
                genre,
                unique_viewers,
                ROUND(total_watch_hours, 2) as total_watch_hours,
                content_count,
                ROUND(total_watch_hours / content_count, 2) as hours_per_content
            FROM netflix_analytics.genre_performance_metrics
            ORDER BY unique_viewers DESC
            LIMIT 5
        """
    }
    
    print("Netflix Content Analytics - Setup Verification\n")
    print("Checking BigQuery views and sample data...\n")
    
    for title, query in verification_queries.items():
        try:
            query_job = client.query(query)
            results = query_job.result()
            
            # Convert results to list of lists for tabulate
            rows = [row.values() for row in results]
            headers = [field.name for field in results.schema]
            
            print(f"\n=== {title} ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            print()
            
        except Exception as e:
            print(f"Error running {title} query: {e}")
            return False
    
    return True

def main():
    try:
        success = run_verification_queries()
        if success:
            print("""
Setup Verification Complete! ✅

Your Netflix Content Analytics platform is successfully set up and contains valid data.
Next steps:
1. Visit https://lookerstudio.google.com/
2. Follow the instructions in dashboard_setup_guide.md to create your dashboard
3. Use the BigQuery views created to build custom visualizations

For any issues or questions, please refer to the README.md file.
""")
        else:
            print("\nSetup verification failed. Please check the error messages above.")
            sys.exit(1)
    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
