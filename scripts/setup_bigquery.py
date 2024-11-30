from google.cloud import bigquery
import json
import os

def create_schema_field(field_def):
    """Create a SchemaField, handling nested fields for RECORD types."""
    field_args = {
        'name': field_def['name'],
        'field_type': field_def['field_type'],
        'mode': field_def['mode']
    }
    
    # Handle nested fields for RECORD type
    if field_def['field_type'] == 'RECORD' and 'fields' in field_def:
        nested_fields = [create_schema_field(f) for f in field_def['fields']]
        field_args['fields'] = nested_fields
    
    return bigquery.SchemaField(**field_args)

def create_dataset_and_tables():
    # Initialize BigQuery client
    client = bigquery.Client()
    
    # Create dataset
    dataset_id = f"{client.project}.netflix_analytics"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    try:
        dataset = client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {dataset_id} created or already exists.")
    except Exception as e:
        print(f"Error creating dataset: {e}")
        return

    # Load schema definitions
    with open('schemas/bigquery_schemas.json', 'r') as f:
        schemas = json.load(f)
    
    # Create tables with schemas
    table_schemas = {
        'contents': schemas['contents_schema'],
        'users': schemas['users_schema'],
        'viewing_events': schemas['viewing_events_schema']
    }
    
    for table_name, schema_def in table_schemas.items():
        table_id = f"{dataset_id}.{table_name}"
        
        # Delete existing table if it exists
        try:
            client.delete_table(table_id)
            print(f"Deleted existing table {table_id}")
        except Exception:
            pass  # Table doesn't exist
            
        # Create schema fields, handling nested structures
        schema = [create_schema_field(field) for field in schema_def]
        
        # Create the table
        table = bigquery.Table(table_id, schema=schema)
        try:
            table = client.create_table(table)
            print(f"Created table {table_id}")
        except Exception as e:
            print(f"Error creating table {table_name}: {e}")

def load_data_to_bigquery():
    client = bigquery.Client()
    dataset_id = f"{client.project}.netflix_analytics"
    
    # Load data from JSON files
    data_files = {
        'contents': 'data/raw/contents.json',
        'users': 'data/raw/users.json',
        'viewing_events': 'data/raw/viewing_events.json'
    }
    
    for table_name, file_path in data_files.items():
        if not os.path.exists(file_path):
            print(f"Data file {file_path} not found.")
            continue
            
        table_id = f"{dataset_id}.{table_name}"
        
        try:
            # Read the JSON data
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Convert to newline-delimited JSON
            newline_json_path = f"{file_path}.ndjson"
            with open(newline_json_path, 'w') as f:
                for item in data:
                    # Convert arrays to strings for REPEATED fields
                    if table_name == 'contents' and 'tags' in item:
                        item['tags'] = list(item['tags'])
                    if table_name == 'users':
                        if 'preferred_genres' in item:
                            item['preferred_genres'] = list(item['preferred_genres'])
                        if 'preferred_languages' in item:
                            item['preferred_languages'] = list(item['preferred_languages'])
                    
                    f.write(json.dumps(item) + '\n')
            
            # Configure job
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
            )
            
            # Load data
            with open(newline_json_path, 'rb') as f:
                load_job = client.load_table_from_file(
                    f,
                    table_id,
                    job_config=job_config
                )
                result = load_job.result()  # Wait for the job to complete
            
            # Clean up temporary file
            os.remove(newline_json_path)
            
            print(f"Loaded {table_name} data to BigQuery successfully.")
            
            # Get the row count
            table = client.get_table(table_id)
            print(f"Loaded {table.num_rows} rows into {table_id}")
            
        except Exception as e:
            print(f"Error loading data to {table_name}: {e}")
            if hasattr(e, 'errors'):
                for error in e.errors:
                    print(f"Error details: {error}")

if __name__ == "__main__":
    print("Setting up BigQuery dataset and tables...")
    create_dataset_and_tables()
    
    print("\nLoading data to BigQuery...")
    load_data_to_bigquery()
