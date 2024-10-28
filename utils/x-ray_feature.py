import requests
import json
import webbrowser

# Superset connection information
SUPERSET_BASE_URL = "http://localhost:5000"
USERNAME = "admin"
PASSWORD = "admin"

# Superset endpoints
LOGIN_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/security/login"
DATASET_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/dataset/"
CHART_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/chart/"
DASHBOARD_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/dashboard/"
EMBED_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/dashboard/embedded"
CSRF_TOKEN_ENDPOINT = f"{SUPERSET_BASE_URL}/api/v1/security/csrf_token/"

# Step 1: Authenticate (session-based auth if not using API key)
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
        
        # Fetch the CSRF token
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

# Step 2: Fetch dataset metadata
def get_dataset_metadata(dataset_id, headers):
    response = requests.get(f"{DATASET_ENDPOINT}{dataset_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch dataset metadata: {response.text}")

# Step 3: Analyze the dataset and determine visualizations
def analyze_dataset_and_generate_visualizations(dataset_metadata):
    columns = dataset_metadata['result']['columns']
    
    visualizations = []
    for column in columns:
        column_name = column['column_name']
        column_type = column['type']

        if 'VARCHAR' in column_type or 'TEXT' in column_type:
            visualizations.append({
                "type": "echarts_area",
                "metric": "count",
                "groupby": column_name,
            })
        elif 'INT' in column_type or 'FLOAT' in column_type:
            visualizations.append({
                "type": "histogram",
                "metric": column_name,
                "all_columns_x": column_name,
                "groupby": column_name
            })
        elif 'DATE' in column_type or 'TIMESTAMP' in column_type:
            visualizations.append({
                "type": "line",
                "metric": column_name,
                "time_column": column_name
            })

    return visualizations

# Step 4: Create a Chart via API
def create_chart(headers, dataset_id, visualization, dashboard_id=None):
    try:
        # Prepare chart parameters based on visualization type
        if visualization['type'] == "histogram":
            params = {
                "x": visualization['metric'],
                "metrics": visualization['metric'],
                "bins": 20,
                "color_scheme": "bnbColors",
                "row_limit": 100,
                "viz_type": visualization['type'],
                "all_columns_x": [visualization['metric']],
            }
        elif visualization['type'] == 'echarts_area':
            params = {
                "metrics": [visualization['metric']],
                "filters": [],
                "row_limit": 100,
                "viz_type": visualization['type'],
                "x_axis_sort_asc": True,
                "x_axis_sort_series": "name",
                "x_axis": visualization.get('groupby'),
            }
        else:
            params = {
                "metrics": [visualization['metric']],
                "groupby": visualization.get('groupby'),
                "filters": [],
                "row_limit": 100,
                "viz_type": visualization['type']
            }
       
        chart_data = {
            "slice_name": f"{visualization['type'].capitalize()} Chart",
            "viz_type": visualization['type'],
            "datasource_id": dataset_id,
            "datasource_type": "table",
            "params": json.dumps(params),
            "dashboards": [dashboard_id] if dashboard_id else []
        }

        response = requests.post(CHART_ENDPOINT, headers=headers, json=chart_data)

        if response.status_code == 201:
            chart_id = response.json()['id']
            print(f"Successfully created chart with ID: {chart_id}")
            return chart_id
        else:
            print(f"Failed to create chart: {response.status_code}, Response: {response.text}")
            return None

    except KeyError as e:
        print(f"KeyError in visualization data: {e}")
        return None

# Step 5: Create Dashboard
def create_dashboard(headers, title):
    payload = {
        "dashboard_title": title,
        "slug": None,
        "owners": [1],
        "published": True,
    }
    response = requests.post(DASHBOARD_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 201:
        dashboard_id = response.json().get("id")
        print(f"Dashboard created with ID: {dashboard_id}")
        return dashboard_id
    else:
        print(f"Failed to create dashboard. Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return None

# Step 6: Generate Embed URL for the Dashboard
def generate_embed_url(dashboard_id, headers):
    embed_endpoint = f"{SUPERSET_BASE_URL}/api/v1/dashboard/{dashboard_id}/embedded"
    embed_payload = {
        "allowed_domains": ["http://localhost"]
    }
    
    response = requests.post(embed_endpoint, headers=headers, json=embed_payload)
    
    if response.status_code == 200:
        embed_uuid = response.json()['result']['uuid']
        print(f"Embed URL generated: {embed_uuid}")
        return embed_uuid
    else:
        print(f"Failed to generate embed URL: {response.status_code}, {response.text}")
        raise Exception(f"Failed to generate embed URL: {response.text}")


# Step 7: Render Template with Embed URL
def render_template(embed_url):
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Embedded Superset Dashboard</title>
    </head>
    <body>
        <h1>Embedded Dashboard</h1>
        <iframe src="{embed_url}" width="100%" height="600px" frameborder="0"></iframe>
    </body>
    </html>
    """
    return template

# Full Workflow
def xray_feature_with_dashboard_embedding(dataset_id, dashboard_title):
    headers = authenticate()
    dataset_metadata = get_dataset_metadata(dataset_id, headers)
    visualizations = analyze_dataset_and_generate_visualizations(dataset_metadata)
    dashboard_id = create_dashboard(headers, dashboard_title)
    
    if dashboard_id:
        chart_ids = [create_chart(headers, dataset_id, viz, dashboard_id) for viz in visualizations]
        chart_ids = [chart_id for chart_id in chart_ids if chart_id is not None]

        # Generate embed URL for the dashboard
        embed_uuid = generate_embed_url(dashboard_id, headers)
        embed_url = f"{SUPERSET_BASE_URL}/superset/dashboard/{dashboard_id}/?guest_token={embed_uuid}"
        if embed_url:
            template = render_template(embed_url)
            with open("embedded_dashboard.html", "w") as file:
                file.write(template)
            print("Embedded dashboard template generated: embedded_dashboard.html")
            webbrowser.open("embedded_dashboard.html")
    else:
        print("Dashboard creation failed.")

# Run the workflow
dataset_id = 2  # Replace with your actual dataset ID
dashboard_title = "Auto-generated Insights Dashboard"
xray_feature_with_dashboard_embedding(dataset_id, dashboard_title)
