# Finding Your Data in Google Cloud Console

## Accessing BigQuery Data

1. **Open Google Cloud Console**
   - Visit: https://console.cloud.google.com
   - Make sure you're signed in with the correct account
   - Select project: "netflix-content-analytics"

2. **Navigate to BigQuery**
   - Click on the navigation menu (☰) in the top-left corner
   - Scroll down to "Analytics" section
   - Click on "BigQuery"
   - Or use direct link: https://console.cloud.google.com/bigquery

3. **Find Your Dataset**
   - In the Explorer panel on the left, expand your project "netflix-content-analytics"
   - You'll see the dataset "netflix_analytics"
   - Click to expand the dataset

4. **View Your Tables**
   You should see these tables:
   - `contents` - Raw content data
   - `users` - User information
   - `viewing_events` - Viewing event data

5. **View Your Views**
   In the same dataset, you'll find these views:
   - `content_performance_metrics`
   - `user_engagement_metrics`
   - `daily_viewing_metrics`
   - `device_performance_metrics`
   - `genre_performance_metrics`

## Querying Your Data

1. **Preview Table Data**
   - Click on any table/view name
   - Select "Preview" tab to see sample data
   - Or click "Query" tab to write SQL queries

2. **Sample Queries**
   Copy and paste these queries in the Query Editor:

   **View Content Data:**
   ```sql
   SELECT *
   FROM `netflix-content-analytics.netflix_analytics.contents`
   LIMIT 1000;
   ```

   **View User Data:**
   ```sql
   SELECT *
   FROM `netflix-content-analytics.netflix_analytics.users`
   LIMIT 1000;
   ```

   **View Events Data:**
   ```sql
   SELECT *
   FROM `netflix-content-analytics.netflix_analytics.viewing_events`
   LIMIT 1000;
   ```

## Data Locations Summary

### Raw Data Tables
- Project: `netflix-content-analytics`
- Dataset: `netflix_analytics`
- Tables:
  * `contents` (~200 rows)
  * `users` (~500 rows)
  * `viewing_events` (~28,000 rows)

### Processed Data (Views)
Same location, with these views:
- `content_performance_metrics`
- `user_engagement_metrics`
- `daily_viewing_metrics`
- `device_performance_metrics`
- `genre_performance_metrics`

## Useful Tips

1. **Table Details**
   - Click on any table/view name
   - Select "Details" tab to see:
     * Row count
     * Table size
     * Schema information
     * Creation time
     * Last modified time

2. **Schema Exploration**
   - Click on any table/view name
   - Select "Schema" tab to see:
     * Field names
     * Data types
     * Field descriptions
     * Nested field structures

3. **Query History**
   - Click "Query history" in the left panel
   - See all previously run queries
   - Rerun or modify past queries

4. **Export Data**
   - Click on any table
   - Click "Export" button
   - Choose export format (CSV, JSON, Avro)
   - Export to Google Cloud Storage or local download

## Troubleshooting

If you don't see your data:
1. Verify you're in the correct project (`netflix-content-analytics`)
2. Check if the dataset name is exactly `netflix_analytics`
3. Ensure all setup scripts ran successfully
4. Check the BigQuery logs for any errors

For any issues, you can rerun the verification script:
```bash
python scripts/verify_setup.py
```

This will confirm if your data is properly loaded and accessible in BigQuery.
