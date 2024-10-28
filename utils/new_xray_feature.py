import requests
import json
import pandas as pd
import sqlalchemy
from sqlalchemy import inspect

SUPERSET_BASE_URL = "http://localhost:5000"
USERNAME = "admin"
PASSWORD = "admin"

LOGIN_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/security/login"
CSRF_TOKEN_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/security/csrf_token/"
DATASET_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/dataset/"
CHART_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/chart/"
DASHBOARD_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/dashboard/"

def authenticate():
    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "provider": "db",
        "refresh": True
    }
    response = requests.post(LOGIN_ENDPOINT, json=login_data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}

        csrf_response = requests.get(CSRF_TOKEN_ENDPOINT, headers=headers)
        if csrf_response.status_code == 200:
            csrf_token = csrf_response.json().get("result")
            headers["X-CSRFToken"] = csrf_token
            headers["Content-Type"] = "application/json"
            return headers
        else:
            raise Exception("Failed to retrieve CSRF token")
    else:
        raise Exception("Authentication failed")

def create_table_if_not_exists(df, engine, table_name):
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        # Create the table based on the DataFrame schema
        df.head(0).to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Table '{table_name}' created.")
    else:
        print(f"Table '{table_name}' already exists.")

def load_json_to_db(file_path, db_connection_string, table_name):
    df = pd.read_json(file_path)
    engine = sqlalchemy.create_engine(db_connection_string)

    # Create table if not exists
    create_table_if_not_exists(df, engine, table_name)

    # Insert data into the table
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Data inserted into '{table_name}' successfully.")
    return df

def get_dataset_id(headers, dataset_name):
    DATASETS_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/dataset/"

    response = requests.get(DATASETS_ENDPOINT, headers=headers)

    if response.status_code == 200:
        datasets = response.json().get("result", [])
        
        for dataset in datasets:
            if dataset.get("table_name") == dataset_name:
                dataset_id = dataset.get("id")
                print(f"Dataset '{dataset_name}' found with ID: {dataset_id}")
                return dataset_id
        
        print(f"Dataset '{dataset_name}' not found.")
        return None
    else:
        print(f"Failed to fetch datasets: {response.text}")
        return None

def create_dataset_in_superset(headers, dataset_name, database_id, schema):
    payload = {
        "database": database_id,
        "table_name": dataset_name,
        "schema": schema
    }

    response = requests.post(DATASET_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 201:
        dataset_id = response.json().get("id")
        print(f"Dataset '{dataset_name}' created with ID: {dataset_id}")
        return dataset_id
    else:
        print(f"Failed to create dataset: {response.text}")
        return None

def analyze_dataset_and_generate_visualizations(df):
    visualizations = []
    datetime_column = None

    table_columns = [{"column_name": col} for col in df.columns]
    visualizations.append({
        "type": "table",
        "columns": table_columns,
        "row_limit": 100,
        "description": "Table visualization of the dataset"
    })

    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            datetime_column = column
            break

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            visualizations.append({
                "type": "histogram",
                "metric": column,
                "all_columns_x": column,
                "description": f"Histogram of {column}"
            })

            # Replace scatter plot with bubble chart
        if pd.api.types.is_numeric_dtype(df[column]) and len(df.columns) > 1:
            # Define the x-axis and y-axis as the first two numeric columns
            x_column = column
            y_column = df.select_dtypes(include='number').columns[1]

            # Define the entity as the first categorical column
            entity_column = df.select_dtypes(include='object').columns[0]

            # Add bubble chart configuration
            if x_column != y_column:
                visualizations.append({
                    "type": "bubble",
                    "x_axis": x_column,
                    "y_axis": y_column,
                    "entity": entity_column,
                    "size": x_column,  # Use x_column as bubble size
                    "description": f"Bubble Chart of {x_column} vs {y_column}"
                })

            visualizations.append({
                "type": "box_plot",
                "all_columns_x": column,
                "metrics": [{"label": column, "expressionType": "SIMPLE", "aggregate": "AVG"}],
                "description": f"Box Plot of {column}"
            })

        if pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
            numeric_column = df.select_dtypes(include='number').columns[0]
            if datetime_column:
                visualizations.append({
                    "type": "bar",
                    "metric": {
                        "label": f"SUM({numeric_column})",
                        "expressionType": "SIMPLE",
                        "column": {"column_name": numeric_column},
                        "aggregate": "SUM"
                    },
                    "groupby": column,
                    "granularity_sqla": datetime_column,
                    "time_range": "No filter",
                    "description": f"Bar Chart of {column} with SUM({numeric_column})"
                })

            numeric_columns = df.select_dtypes(include='number').columns[:3]
            metric = {
                "aggregate": "COUNT",
                "column": {
                    "column_name": column,
                    "filterable": True,
                    "groupby": True,
                    "type": "VARCHAR(50)"
                },
                "expressionType": "SIMPLE",
                "label": f"COUNT({column})"
            }
            visualizations.append({
                "type": "pie",
                "metric": metric,
                "groupby": column,
                "adhoc_filters": [
                    {
                        "clause": "WHERE",
                        "comparator": "No filter",
                        "expressionType": "SIMPLE",
                        "operator": "TEMPORAL_RANGE",
                        "subject": datetime_column if datetime_column else "order_date"
                    }
                ],
                "description": f"Pie Chart of {column} with COUNT({column})",
                "sort_by_metric": True,
                "innerRadius": 30,
                "outerRadius": 70,
                "show_legend": True,
                "show_labels": True,
                "row_limit": 100,
                "color_scheme": "supersetColors"
            })


        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            visualizations.append({
                "type": "line",
                "metric": column,
                "time_column": column,
                "description": f"Time-series Line Chart of {column}"
            })

            visualizations.append({
                "type": "area",
                "metric": column,
                "time_column": column,
                "description": f"Time-series Area Chart of {column}"
            })

    return visualizations


def create_chart(headers, dataset_id, visualization, dashboard_id=None):
    params = {
        "row_limit": 100,
        "viz_type": visualization.get("type")
    }

    if visualization.get("type") == "bubble":
        # Configure x-axis, y-axis, entity, and bubble size
        params.update({
            "x": {
                "expressionType": "SIMPLE",
                "column": {"column_name": visualization.get("x_axis")},
                "aggregate": "SUM",  # Adjust as needed
                "label": f"SUM({visualization.get('x_axis')})"
            },
            "y": {
                "expressionType": "SIMPLE",
                "column": {"column_name": visualization.get("y_axis")},
                "aggregate": "SUM",  # Adjust as needed
                "label": f"SUM({visualization.get('y_axis')})"
            },
            "entity": visualization.get("entity"),
            "size": {
                "expressionType": "SIMPLE",
                "column": {"column_name": visualization.get("size")},
                "aggregate": "MAX",  # Adjust as needed
                "label": f"MAX({visualization.get('size')})"
            },
            "max_bubble_size": 25,
            "color_scheme": "supersetColors",
            "show_legend": True
        })
    
    elif visualization.get("type") == "table":
        params.update({
            "all_columns": [col["column_name"] for col in visualization.get("columns")],
            "granularity_sqla": None,  # No time-based granularity for tables
            "adhoc_filters": [],
            "sort_by": None,
            "table_timestamp_format": "smart_date"
        })

    elif visualization.get("type") == "box_plot":
        params.update({
            "all_columns_x": [visualization.get("all_columns_x")],
            "metrics": [
                {
                    "label": visualization.get("all_columns_x"),
                    "expressionType": "SIMPLE",
                    "column": {
                        "column_name": visualization.get("all_columns_x")
                    },
                    "aggregate": "AVG"  # Adjust the aggregation as needed
                }
            ]
        })

    elif visualization.get("type") == "bar":
        if visualization.get("granularity_sqla"):
            params.update({
                "metrics": [
                    {
                        "label": visualization["metric"]["label"],
                        "expressionType": visualization["metric"]["expressionType"],
                        "column": visualization["metric"]["column"],
                        "aggregate": visualization["metric"]["aggregate"]
                    }
                ],
                "groupby": [visualization.get("groupby")],
                "granularity_sqla": visualization.get("granularity_sqla"),
                "time_range": visualization.get("time_range")
            })

    elif visualization.get("type") in ["histogram"]:
        params["all_columns_x"] = [visualization.get("all_columns_x")]

    elif visualization.get("type") in ["pie"]:
        params.update({
        "metric": {
            "label": visualization["metric"]["label"],
            "expressionType": visualization["metric"]["expressionType"],
            "column": visualization["metric"]["column"],
            "aggregate": visualization["metric"]["aggregate"]
        },
        "groupby": [visualization.get("groupby")],
        "sort_by_metric": visualization.get("sort_by_metric", True),
        "adhoc_filters": visualization.get("adhoc_filters")
        })


    elif visualization.get("type") in ["line", "area"]:
        params["granularity_sqla"] = visualization.get("time_column")
        params["time_range"] = "No Filter"

    elif visualization.get("type") == "big_number":
        params["metric"] = visualization.get("metric")

    chart_data = {
        "slice_name": visualization.get("description"),
        "viz_type": visualization.get("type"),
        "datasource_id": dataset_id,
        "datasource_type": "table",
        "params": json.dumps(params),
        "dashboards": [dashboard_id] if dashboard_id else []
    }

    response = requests.post(CHART_ENDPOINT, headers=headers, json=chart_data)
    if response.status_code == 201:
        chart_id = response.json().get("id")
        print(f"Chart '{visualization['description']}' created with ID: {chart_id}")
        return chart_id
    else:
        print(f"Failed to create chart: {response.text}")
        return None


def create_dashboard(headers, title):
    payload = {
        "dashboard_title": title,
        "published": True
    }

    response = requests.post(DASHBOARD_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 201:
        dashboard_id = response.json().get("id")
        print(f"Dashboard '{title}' created with ID: {dashboard_id}")
        return dashboard_id
    else:
        print(f"Failed to create dashboard: {response.text}")
        return None

def run_xray_with_json(file_path, db_connection_string, table_name, dataset_name, dashboard_title, database_id, schema):
    headers = authenticate()

    df = load_json_to_db(file_path, db_connection_string, table_name)

    dataset_id = get_dataset_id(headers, dataset_name)
    if not dataset_id:
        dataset_id = create_dataset_in_superset(headers, table_name, database_id, schema)

    if dataset_id:
        visualizations = analyze_dataset_and_generate_visualizations(df)
        dashboard_id = create_dashboard(headers, dashboard_title)

        if dashboard_id:
            for viz in visualizations:
                create_chart(headers, dataset_id, viz, dashboard_id)



# Example usage
json_file = 'employee.json'  # Replace with your JSON file path
db_connection_string = 'mysql+pymysql://superset_user3:dhatchan@localhost/superset_dbb'
table_name = 'employee'
dataset_name = 'employee'
dashboard_title = 'Auto-generated JSON Dashboard'
database_id = 1  # Replace with the actual Superset database ID
schema = 'superset_dbb'  # Replace with your actual schema

run_xray_with_json(json_file, db_connection_string, table_name, dataset_name, dashboard_title, database_id, schema)
