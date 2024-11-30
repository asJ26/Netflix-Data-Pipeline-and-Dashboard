# Netflix Streaming Analytics - Technical Report

## Project Overview
This project implements a comprehensive streaming analytics pipeline that processes and visualizes Netflix-style streaming data using Google Cloud Platform (BigQuery) for data processing and Plotly for interactive visualizations.

## Data Architecture

### 1. Data Volume
- Content Library: 50 titles across multiple genres
- User Base: 1000 users with diverse demographics
- Streaming Events: 10,000 viewing events

### 2. Data Distribution

#### Content Distribution
- Top Genres:
  * Romance (8 titles, avg duration: 86.6 min)
  * Adventure (5 titles, avg duration: 70.2 min)
  * Sci-Fi (5 titles, avg duration: 105.0 min)
- Content Types: Mix of movies and series
- Languages: 12 different languages
- Ratings: G through TV-MA

#### User Demographics
- Subscription Distribution:
  * Standard: 37.4% (374 users)
  * Basic: 26.0% (260 users)
  * Premium: 19.6% (196 users)
  * Student: 8.6% (86 users)
  * Family: 8.4% (84 users)
- Geographic Spread: 20 countries
- Age Groups: 13-17 through 65+

#### Viewing Patterns
- Device Usage:
  * Smart TV: 21.85% (2,185 events)
  * Desktop: 20.17% (2,017 events)
  * Mobile: 16.66% (1,666 events)
  * Tablet: 16.62% (1,662 events)
  * Streaming Stick: 12.54% (1,254 events)
  * Gaming Console: 12.16% (1,216 events)

### 3. Quality Metrics
- Bandwidth Performance:
  * Smart TV: 36.4 Mbps
  * Desktop: 33.5 Mbps
  * Gaming Console: 35.1 Mbps
  * Mobile Devices: ~26.5 Mbps
- Completion Rates:
  * Consistent across devices (61-62%)
  * Slightly higher on gaming consoles (62.56%)

## Key Insights

### 1. Streaming Quality
- Higher bandwidth utilization on fixed devices
- Mobile devices show optimized bandwidth usage
- Buffering events correlate with connection types
- Audio quality remains consistent across devices

### 2. User Engagement
- Premium subscribers show 20% higher engagement
- Content in preferred languages shows 10% higher completion rates
- Genre matching increases engagement by 15-20%
- Family plan users prefer smart TV viewing

### 3. Content Performance
- Romance and Adventure genres lead in volume
- Sci-Fi shows longer average watch duration
- Thrillers have highest average duration (151.7 min)
- Family content shows balanced device distribution

### 4. Technical Performance
- Connection type significantly impacts quality:
  * 5G/Ethernet: 0-2 buffering events
  * 4G: 1-4 buffering events
  * 3G: 2-7 buffering events
- Device-specific optimizations visible in metrics
- Smart TV leads in both quantity and quality of streams

## Implementation Details

### 1. Data Processing
- Implemented in BigQuery for scalability
- Materialized views for efficient querying
- Real-time capable data pipeline
- Optimized for large-scale analytics

### 2. Visualization Pipeline
- Interactive dashboards using Plotly
- Netflix-styled dark theme
- Responsive design
- Multiple visualization types:
  * Heatmaps for correlation analysis
  * Box plots for distribution analysis
  * Time series for trend analysis
  * Bubble charts for multi-dimensional analysis

### 3. Analytics Features
- Quality metrics analysis
- User engagement tracking
- Content performance metrics
- Recommendation system analysis
- Device and platform analytics

## Future Enhancements
1. Real-time streaming data integration
2. Machine learning for predictive analytics
3. A/B testing framework integration
4. Enhanced recommendation analytics
5. Geographic performance analysis
6. Content acquisition insights
