from google.cloud import bigquery

def check_data_distribution():
    client = bigquery.Client()
    dataset_id = f"{client.project}.netflix_analytics"
    
    print("\nData Distribution Analysis:")
    print("=" * 50)
    
    # Basic counts
    counts_query = f"""
    SELECT 
        (SELECT COUNT(*) FROM `{dataset_id}.contents`) as content_count,
        (SELECT COUNT(*) FROM `{dataset_id}.users`) as user_count,
        (SELECT COUNT(*) FROM `{dataset_id}.viewing_events`) as event_count
    """
    
    results = client.query(counts_query).result()
    for row in results:
        print(f"\nTotal Counts:")
        print(f"Contents: {row.content_count}")
        print(f"Users: {row.user_count}")
        print(f"Viewing Events: {row.event_count}")
    
    # Content distribution
    content_query = f"""
    SELECT 
        genre,
        COUNT(*) as count,
        AVG(duration_minutes) as avg_duration
    FROM `{dataset_id}.contents`
    GROUP BY genre
    ORDER BY count DESC
    LIMIT 10
    """
    
    print("\nContent Distribution by Genre:")
    print("-" * 40)
    results = client.query(content_query).result()
    for row in results:
        print(f"{row.genre}: {row.count} titles (avg duration: {row.avg_duration:.1f} min)")
    
    # User distribution
    user_query = f"""
    SELECT 
        subscription_type,
        COUNT(*) as count,
        COUNT(DISTINCT country) as countries
    FROM `{dataset_id}.users`
    GROUP BY subscription_type
    ORDER BY count DESC
    """
    
    print("\nUser Distribution by Subscription:")
    print("-" * 40)
    results = client.query(user_query).result()
    for row in results:
        print(f"{row.subscription_type}: {row.count} users across {row.countries} countries")
    
    # Viewing patterns
    viewing_query = f"""
    SELECT 
        device_type,
        COUNT(*) as event_count,
        AVG(quality_metrics.bandwidth_mbps) as avg_bandwidth,
        AVG(engagement_signals.completion_rate) as avg_completion
    FROM `{dataset_id}.viewing_events`
    GROUP BY device_type
    ORDER BY event_count DESC
    """
    
    print("\nViewing Patterns by Device:")
    print("-" * 40)
    results = client.query(viewing_query).result()
    for row in results:
        print(f"{row.device_type}:")
        print(f"  Events: {row.event_count}")
        print(f"  Avg Bandwidth: {row.avg_bandwidth:.1f} Mbps")
        print(f"  Avg Completion: {row.avg_completion:.2%}")

if __name__ == "__main__":
    check_data_distribution()
