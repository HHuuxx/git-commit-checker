import requests
import base64
from environ import Env

# Initialize the environment variable reader
env = Env()
env.read_env()

# Jira server URL, username, and API token (or password)
JIRA_SERVER = env.str("JIRA_SERVER")
JIRA_USERNAME = env.str("JIRA_USERNAME")
JIRA_API_TOKEN = env.str("JIRA_API_TOKEN")

# Endpoint to fetch all boards
boards_endpoint = f'{JIRA_SERVER}/rest/agile/1.0/board'

# Set up authentication headers
auth_headers = {
    'Authorization': f'Basic {base64.b64encode(f"{JIRA_USERNAME}:{JIRA_API_TOKEN}".encode()).decode()}'
}

# Send GET request to fetch board data
response = requests.get(boards_endpoint, headers=auth_headers)

if response.status_code == 200:
    boards_data = response.json()
    for board in boards_data['values']:
        print(f"Board ID: {board['id']}, Board Name: {board['name']}")
else:
    print(f"Failed to fetch boards. Status code: {response.status_code}")
