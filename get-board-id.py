import requests
import base64

# Jira server URL, username, and API token (or password)
JIRA_SERVER = 'https://smarterlaunch.atlassian.net/'
JIRA_USERNAME = 'allen.antipuesto@smarterlaunch.com'
JIRA_API_TOKEN = 'ATATT3xFfGF0aOuHlM8fet3jDKsQMl3Jgp9DWWCWSR3b9mxMaw7evlUhukJm0yG8V1oPlEHplP3oCiahymV7ocq4qpd56Rw-4aQd9cCSgAhtWTQSfA0K7uaR7_39-kdtSAXiM4a8yy5_-CsDfmgvvBPBp3Vdwa3bRnF2Uxs2BLGDSs08Ewdo7Ao=47369387'

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
