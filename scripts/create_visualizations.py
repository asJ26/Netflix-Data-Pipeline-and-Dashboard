from google.cloud import bigquery
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

def get_bigquery_client():
    return bigquery.Client()

def query_quality_metrics():
    client = get_bigquery_client()
    query = """
    SELECT *
    FROM netflix_analytics.quality_metrics_view
    """
    return client.query(query).to_dataframe()

def query_engagement_metrics():
    client = get_bigquery_client()
    query = """
    SELECT *
    FROM netflix_analytics.engagement_metrics_view
    """
    return client.query(query).to_dataframe()

def query_ratings_data():
    client = get_bigquery_client()
    query = """
    SELECT *
    FROM netflix_analytics.ratings_analysis_view
    """
    return client.query(query).to_dataframe()

def query_recommendation_effectiveness():
    client = get_bigquery_client()
    query = """
    SELECT *
    FROM netflix_analytics.recommendation_analysis_view
    """
    return client.query(query).to_dataframe()

def create_quality_metrics_visualization(df):
    # Create a more comprehensive quality metrics dashboard
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "Buffering Events by Device & Connection",
            "Bandwidth Distribution by Device",
            "Startup Time by Connection Type",
            "Frames Dropped Ratio",
            "Audio Quality Score",
            "Session Distribution"
        ),
        specs=[
            [{"type": "heatmap"}, {"type": "box"}],
            [{"type": "bar"}, {"type": "violin"}],
            [{"type": "bar"}, {"type": "domain"}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )

    # Buffering Events Heatmap
    pivot_buffer = df.pivot_table(
        values='avg_buffering',
        index='device_type',
        columns='connection_type',
        aggfunc='mean'
    ).fillna(0)
    
    fig.add_trace(
        go.Heatmap(
            z=pivot_buffer.values,
            x=pivot_buffer.columns,
            y=pivot_buffer.index,
            colorscale='RdYlBu_r'
        ),
        row=1, col=1
    )

    # Bandwidth Box Plot
    fig.add_trace(
        go.Box(
            x=df['device_type'],
            y=df['avg_bandwidth'],
            name="Bandwidth"
        ),
        row=1, col=2
    )

    # Startup Time by Connection
    startup_by_conn = df.groupby('connection_type')['avg_startup_time'].mean().reset_index()
    fig.add_trace(
        go.Bar(
            x=startup_by_conn['connection_type'],
            y=startup_by_conn['avg_startup_time'],
            name="Startup Time"
        ),
        row=2, col=1
    )

    # Frames Dropped
    fig.add_trace(
        go.Violin(
            x=df['device_type'],
            y=df['avg_frames_dropped'],
            name="Frames Dropped"
        ),
        row=2, col=2
    )

    # Audio Quality
    fig.add_trace(
        go.Bar(
            x=df['device_type'],
            y=df['avg_audio_quality'],
            name="Audio Quality"
        ),
        row=3, col=1
    )

    # Session Distribution
    fig.add_trace(
        go.Pie(
            labels=df['device_type'],
            values=df['session_count'],
            name="Sessions"
        ),
        row=3, col=2
    )

    fig.update_layout(
        height=1200,
        showlegend=False,
        title_text="Streaming Quality Analysis Dashboard",
        template="plotly_dark"
    )
    
    fig.write_html("data/processed/visualizations/quality_metrics.html")

def create_engagement_visualization(df):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Engagement Score by Device",
            "Completion Rate Distribution",
            "Watch Duration by Device",
            "High Engagement Distribution"
        ),
        specs=[
            [{"type": "box"}, {"type": "violin"}],
            [{"type": "bar"}, {"type": "domain"}]
        ]
    )

    # Engagement Score
    fig.add_trace(
        go.Box(
            x=df['device_type'],
            y=df['avg_engagement'],
            name="Engagement"
        ),
        row=1, col=1
    )

    # Completion Rate
    fig.add_trace(
        go.Violin(
            x=df['device_type'],
            y=df['avg_completion'],
            name="Completion"
        ),
        row=1, col=2
    )

    # Watch Duration
    fig.add_trace(
        go.Bar(
            x=df['device_type'],
            y=df['avg_duration'],
            name="Duration"
        ),
        row=2, col=1
    )

    # High Engagement Distribution
    fig.add_trace(
        go.Pie(
            labels=df['device_type'],
            values=df['high_engagement_ratio'],
            name="High Engagement"
        ),
        row=2, col=2
    )

    fig.update_layout(
        height=800,
        title_text="User Engagement Analysis",
        template="plotly_dark"
    )
    
    fig.write_html("data/processed/visualizations/engagement_metrics.html")

def create_ratings_visualization(df):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Genre Performance Bubble Chart",
            "Content Distribution by Type",
            "Average Ratings by Genre",
            "Engagement vs Ratings"
        ),
        specs=[
            [{"type": "scatter"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "scatter"}]
        ]
    )

    # Genre Performance Bubble Chart
    fig.add_trace(
        go.Scatter(
            x=df['content_count'],
            y=df['avg_rating'],
            mode='markers',
            marker=dict(
                size=df['total_views'] / df['total_views'].max() * 50,
                color=df['avg_engagement'],
                colorscale='Viridis',
                showscale=True,
                sizemode='area'
            ),
            text=df['genre'],
            hovertemplate="Genre: %{text}<br>Content Count: %{x}<br>Avg Rating: %{y:.2f}<extra></extra>"
        ),
        row=1, col=1
    )

    # Content Distribution by Type
    type_dist = df.groupby('type').agg({
        'content_count': 'sum',
        'total_views': 'sum'
    }).reset_index()
    
    fig.add_trace(
        go.Bar(
            x=type_dist['type'],
            y=type_dist['content_count'],
            name="Content Count"
        ),
        row=1, col=2
    )

    # Average Ratings by Genre
    fig.add_trace(
        go.Bar(
            x=df['genre'],
            y=df['avg_rating'],
            name="Avg Rating"
        ),
        row=2, col=1
    )

    # Engagement vs Ratings Scatter
    fig.add_trace(
        go.Scatter(
            x=df['avg_engagement'],
            y=df['avg_rating'],
            mode='markers+text',
            text=df['genre'],
            textposition="top center",
            name="Genre Performance"
        ),
        row=2, col=2
    )

    fig.update_layout(
        height=1000,
        title_text="Content Ratings Analysis",
        template="plotly_dark",
        showlegend=True
    )
    
    fig.write_html("data/processed/visualizations/ratings_analysis.html")

def create_recommendation_visualization(df):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Algorithm Effectiveness Heatmap",
            "Top 10 Engagement Rate by Algorithm",
            "Category Performance",
            "Rating Distribution"
        ),
        specs=[
            [{"type": "heatmap"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "box"}]
        ]
    )

    # Algorithm Effectiveness Heatmap
    pivot_rec = df.pivot_table(
        values='avg_engagement',
        index='algorithm_type',
        columns='recommendation_category',
        aggfunc='mean'
    ).fillna(0)
    
    fig.add_trace(
        go.Heatmap(
            z=pivot_rec.values,
            x=pivot_rec.columns,
            y=pivot_rec.index,
            colorscale='Viridis'
        ),
        row=1, col=1
    )

    # Top 10 Engagement Rate
    algo_perf = df.groupby('algorithm_type')['top_10_engagement_rate'].mean().reset_index()
    fig.add_trace(
        go.Bar(
            x=algo_perf['algorithm_type'],
            y=algo_perf['top_10_engagement_rate'],
            name="Top 10 Rate"
        ),
        row=1, col=2
    )

    # Category Performance
    cat_perf = df.groupby('recommendation_category')['avg_engagement'].mean().reset_index()
    fig.add_trace(
        go.Bar(
            x=cat_perf['recommendation_category'],
            y=cat_perf['avg_engagement'],
            name="Category Engagement"
        ),
        row=2, col=1
    )

    # Rating Distribution
    fig.add_trace(
        go.Box(
            x=df['recommendation_category'],
            y=df['avg_rating'],
            name="Ratings"
        ),
        row=2, col=2
    )

    fig.update_layout(
        height=1000,
        title_text="Recommendation System Analysis",
        template="plotly_dark"
    )
    
    fig.write_html("data/processed/visualizations/recommendation_effectiveness.html")

def main():
    try:
        # Create quality metrics visualization
        quality_df = query_quality_metrics()
        create_quality_metrics_visualization(quality_df)

        # Create engagement visualization
        engagement_df = query_engagement_metrics()
        create_engagement_visualization(engagement_df)

        # Create ratings visualization
        ratings_df = query_ratings_data()
        create_ratings_visualization(ratings_df)

        # Create recommendation effectiveness visualization
        recommendation_df = query_recommendation_effectiveness()
        create_recommendation_visualization(recommendation_df)

        print("Visualizations have been created successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
