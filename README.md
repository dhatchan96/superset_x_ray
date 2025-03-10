
# Superset X-Ray Feature

This project enhances **Apache Superset** with an "X-Ray" feature inspired by **Metabase's X-Ray**, which analyzes datasets and generates automatic visualizations, including charts, dashboards, and table views.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Running Superset](#running-superset)
- [Using X-Ray Feature](#using-x-ray-feature)
- [Embedding Dashboards](#embedding-dashboards)
- [Pushing Code to a New Repository](#pushing-code-to-a-new-repository)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Requirements
- Python 3.8 or higher
- Node.js 14.x or higher
- Yarn 1.x
- MySQL (for backend database)
- Git

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/dhatchan96/superset_x_ray.git
cd superset_x_ray
```

### 2. Set Up Python Environment
Create and activate a virtual environment:
```bash
python -m venv superset-env
source superset-env/bin/activate  # On Windows: .\superset-env\Scripts\activate
```

### 3. Install Python Dependencies
Install Superset and its dependencies:
```bash
pip install -e .
```

### 4. Install Frontend Dependencies
Navigate to the frontend folder and install required packages:
```bash
cd superset-frontend
yarn install
```

### 5. Build the Frontend
Build the frontend assets:
```bash
yarn run build
```
For development:
```bash
yarn run dev-server
```

## Setup

### 1. Initialize Superset Database
```bash
superset db upgrade
```

### 2. Create Admin User
Set up an admin user for Superset:
```bash
export FLASK_APP=superset
superset fab create-admin
```

### 3. Start Superset Server
Run the Superset server:
```bash
flask --app=superset run -p 5000
```

### 4. Configure MySQL Database
Update `superset_config.py` with your MySQL database URI:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@<hostname>:<port>/<database>'
```
Replace `<username>`, `<password>`, `<hostname>`, `<port>`, and `<database>` with your credentials.

### 5. Connect to MySQL Database in Superset
1. Go to **Data** > **Databases** in Superset UI.
2. Add a new connection for MySQL using the provided credentials.

## Running Superset
Run Superset using the following command:
```bash
superset run -p 8088 --with-threads --reload --debugger
```

## Using X-Ray Feature

### 1. Run the X-Ray Script
Use the `xray_feature.py` script to analyze datasets and generate visualizations.
1. Set Superset connection details (username, password, URL) in the script.
2. Run the script:
   ```bash
   python utils/xray_feature.py
   ```

### 2. Sample JSON Dataset
To test the X-Ray feature, you can use the following dataset:
```json
[
  {
    "employee_id": 1,
    "name": "Alice",
    "age": 29,
    "department": "Engineering",
    "salary": 75000,
    "hire_date": "2022-03-15",
    "is_manager": false
  },
  {
    "employee_id": 2,
    "name": "Bob",
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "hire_date": "2019-08-01",
    "is_manager": true
  }
]
```
Save this as a `.json` file and update the X-Ray script with the file path.

## Embedding Dashboards
1. Use Superset's API to generate guest tokens.
2. Ensure `X-Frame-Options` is set to **ALLOWALL** in `superset_config.py`:
   ```python
   TEMPLATES_AUTO_RELOAD = True
   WTF_CSRF_ENABLED = False
   FEATURE_FLAGS = {
       "ALLOWED_FRAME_ORIGINS": ["*"]
   }
   ```
3. Use the generated guest token to create an embedded dashboard in an iframe.

## Pushing Code to a New Repository

### 1. Add a New Remote
If you want to push your code to a new GitHub repository:
```bash
git remote set-url origin https://github.com/yourusername/new-repo.git
```

### 2. Push the Code
If the branch is named **main**:
```bash
git push -u origin main
```
If it is **master**:
```bash
git push -u origin master
```

## Troubleshooting

### Common Issues
1. **ModuleNotFoundError**: Ensure all dependencies are installed and the virtual environment is activated.
2. **CSRF Token Missing**: Set `WTF_CSRF_ENABLED = False` in `superset_config.py`.
3. **Refused to display in iframe**: Set `X-Frame-Options` to **ALLOWALL** in the Superset config.

### General Tips
- If Superset commands don’t work, use `flask --app=superset run`.
- Use `superset db upgrade` for database migrations.

## Contributing
Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the Apache License 2.0.
