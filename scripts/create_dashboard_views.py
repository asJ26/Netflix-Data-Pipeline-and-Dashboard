from google.cloud import bigquery

def create_bigquery_views():
    client = bigquery.Client()
    dataset_id = f"{client.project}.netflix_analytics"

    # Create materialized view for quality metrics
    quality_metrics_view = f"""
    CREATE OR REPLACE VIEW `{dataset_id}.quality_metrics_view` AS
    WITH device_metrics AS (
        SELECT 
            device_type,
            quality_metrics.connection_type,
            quality_metrics.buffering_events,
            quality_metrics.bandwidth_mbps,
            quality_metrics.startup_time_seconds,
            quality_metrics.frames_dropped_ratio,
            quality_metrics.audio_quality_score,
            FIRST_VALUE(timestamp) OVER (PARTITION BY device_type ORDER BY timestamp) as first_seen,
            COUNT(*) OVER (PARTITION BY device_type) as total_sessions
        FROM `{dataset_id}.viewing_events`
    )
    SELECT 
        device_type,
        connection_type,
        AVG(buffering_events) as avg_buffering,
        AVG(bandwidth_mbps) as avg_bandwidth,
        AVG(startup_time_seconds) as avg_startup_time,
        AVG(frames_dropped_ratio) as avg_frames_dropped,
        AVG(audio_quality_score) as avg_audio_quality,
        COUNT(*) as session_count,
        MAX(total_sessions) as total_device_sessions
    FROM device_metrics
    GROUP BY device_type, connection_type
    """

    # Create materialized view for engagement metrics
    engagement_view = f"""
    CREATE OR REPLACE VIEW `{dataset_id}.engagement_metrics_view` AS
    WITH engagement_stats AS (
        SELECT 
            device_type,
            quality_metrics.connection_type,
            engagement_signals.engagement_score,
            engagement_signals.completion_rate,
            watch_duration_seconds,
            PERCENT_RANK() OVER (PARTITION BY device_type ORDER BY engagement_signals.engagement_score) as engagement_percentile
        FROM `{dataset_id}.viewing_events`
    )
    SELECT 
        device_type,
        connection_type,
        AVG(engagement_score) as avg_engagement,
        AVG(completion_rate) as avg_completion,
        AVG(watch_duration_seconds) as avg_duration,
        COUNT(*) as session_count,
        AVG(CASE WHEN engagement_percentile >= 0.9 THEN 1 ELSE 0 END) as high_engagement_ratio
    FROM engagement_stats
    GROUP BY device_type, connection_type
    """

    # Create materialized view for ratings analysis
    ratings_view = f"""
    CREATE OR REPLACE VIEW `{dataset_id}.ratings_analysis_view` AS
    WITH content_ratings AS (
        SELECT 
            c.content_id,
            c.type,
            c.genre,
            c.title,
            v.engagement_signals.rating_given,
            v.engagement_signals.engagement_score,
            COUNT(*) OVER (PARTITION BY c.content_id) as view_count,
            AVG(v.engagement_signals.rating_given) OVER (PARTITION BY c.genre) as genre_avg_rating
        FROM `{dataset_id}.contents` c
        JOIN `{dataset_id}.viewing_events` v
        ON c.content_id = v.content_id
    )
    SELECT 
        type,
        genre,
        AVG(CASE WHEN rating_given IS NOT NULL THEN rating_given ELSE 0 END) as avg_rating,
        COUNT(DISTINCT content_id) as content_count,
        SUM(view_count) as total_views,
        AVG(engagement_score) as avg_engagement,
        AVG(genre_avg_rating) as genre_rating
    FROM content_ratings
    GROUP BY type, genre
    """

    # Create materialized view for recommendation analysis
    recommendation_view = f"""
    CREATE OR REPLACE VIEW `{dataset_id}.recommendation_analysis_view` AS
    WITH recommendation_metrics AS (
        SELECT 
            recommendation_data.algorithm_type,
            recommendation_data.recommendation_category,
            recommendation_data.recommendation_score,
            engagement_signals.engagement_score,
            engagement_signals.rating_given,
            ROW_NUMBER() OVER (PARTITION BY recommendation_data.algorithm_type 
                             ORDER BY engagement_signals.engagement_score DESC) as rank_by_engagement
        FROM `{dataset_id}.viewing_events`
    )
    SELECT 
        algorithm_type,
        recommendation_category,
        AVG(recommendation_score) as avg_rec_score,
        AVG(engagement_score) as avg_engagement,
        AVG(CASE WHEN rating_given IS NOT NULL THEN rating_given ELSE 0 END) as avg_rating,
        COUNT(*) as recommendation_count,
        AVG(CASE WHEN rank_by_engagement <= 10 THEN 1 ELSE 0 END) as top_10_engagement_rate
    FROM recommendation_metrics
    GROUP BY algorithm_type, recommendation_category
    """

    # Execute view creation queries
    views = {
        'quality_metrics_view': quality_metrics_view,
        'engagement_metrics_view': engagement_view,
        'ratings_analysis_view': ratings_view,
        'recommendation_analysis_view': recommendation_view
    }

    for view_name, query in views.items():
        try:
            query_job = client.query(query)
            query_job.result()
            print(f"Successfully created view: {view_name}")
        except Exception as e:
            print(f"Error creating view {view_name}: {str(e)}")

if __name__ == "__main__":
    create_bigquery_views()
