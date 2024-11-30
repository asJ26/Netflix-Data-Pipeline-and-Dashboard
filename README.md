# Netflix Streaming Analytics Platform

A comprehensive analytics platform for processing and visualizing streaming service data using Google Cloud Platform (BigQuery) and interactive visualizations.

## Data Volume
- 10,000 diverse users across 20 countries
- 200 content items across 14 genres
- 100,000 viewing events with detailed metrics

## Project Structure

```
├── data/
│   ├── processed/           # Processed data and visualizations
│   ├── raw/                # Raw JSON data files
│   └── reference/          # Reference data
├── schemas/                # BigQuery schema definitions
├── scripts/               
│   ├── process_streaming_data.py    # Main data processing script
│   ├── create_visualizations.py     # Visualization generation
│   ├── create_dashboard_views.py    # BigQuery views setup
│   ├── setup_bigquery.py           # BigQuery initialization
│   ├── check_data_counts.py        # Data validation
│   └── advanced_analytics.py       # Advanced analysis scripts
└── requirements.txt        # Python dependencies
```

## Features

- Real-time streaming data processing
- Interactive dashboards for:
  * Streaming quality metrics
  * User engagement analysis
  * Content performance
  * Recommendation effectiveness
- BigQuery integration for scalable data processing
- Customizable visualization components
- Comprehensive analytics views

## Key Metrics

### Content Distribution
- 200 titles across 14 genres
- Animation (23 titles)
- Thriller (21 titles)
- Crime (18 titles)
- Average duration: 70-100 minutes

### User Demographics
- Standard plan: 38.88% (3,888 users)
- Basic plan: 26.07% (2,607 users)
- Premium plan: 18.32% (1,832 users)
- Family plan: 8.88% (888 users)
- Student plan: 7.85% (785 users)

### Viewing Patterns
- Smart TV: 22.07% (22,065 events)
- Desktop: 19.42% (19,424 events)
- Mobile: 17.01% (17,012 events)
- Tablet: 16.88% (16,879 events)
- Gaming/Streaming: ~24.6% (24,620 events)

## Prerequisites

- Python 3.8+
- Google Cloud Platform account
- BigQuery enabled in your GCP project
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd netflix-analytics
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

## Usage

1. Generate and process sample data:
```bash
python scripts/process_streaming_data.py
```

2. View data distribution:
```bash
python scripts/check_data_counts.py
```

3. Access visualizations:
- Open `data/processed/visualizations/dashboard.html` in a web browser

## Data Processing Pipeline

1. Data Generation
- Creates realistic streaming events
- Simulates user behavior patterns
- Generates quality metrics

2. BigQuery Processing
- Creates optimized tables
- Implements materialized views
- Performs complex aggregations

3. Visualization Generation
- Interactive Plotly dashboards
- Netflix-styled theming
- Multiple visualization types

## Analytics Components

### Quality Metrics
- Buffering events analysis
- Bandwidth utilization
- Startup time tracking
- Frame drop analysis

### User Engagement
- Watch duration patterns
- Completion rates
- Device preferences
- Interaction tracking

### Content Analysis
- Genre performance
- Language distribution
- Rating patterns
- Duration analysis

### Technical Performance
- Device-specific metrics
- Connection type analysis
- Quality distribution
- Error rate tracking

## Configuration

Key configuration files:
- `schemas/bigquery_schemas.json`: Define BigQuery table structures
- `scripts/create_dashboard_views.py`: Configure analytics views
- `scripts/create_visualizations.py`: Customize visualization settings

## Development

To extend the platform:

1. Add new metrics:
- Update BigQuery schemas
- Modify data generation logic
- Add visualization components

2. Create new visualizations:
- Add visualization functions in create_visualizations.py
- Update dashboard.html template
- Configure new BigQuery views if needed

3. Implement new analytics:
- Create new analysis scripts
- Add corresponding BigQuery views
- Update visualization pipeline


## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
