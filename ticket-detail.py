import os
import json
import requests
from environ import Env

# Load environment variables
env = Env()
env.read_env()

# Create "tickets" folder if it doesn't exist
if not os.path.exists("tickets"):
    os.makedirs("tickets")

# Jira API URLs
ticket_id = input("Enter the ticket ID: ")
ticket_url = f"{env.str('JIRA_SERVER')}/rest/api/3/issue/{ticket_id}"

# Headers for authentication and JSON content
headers = {
    "Accept": "application/json",
}

# Authenticate using basic authentication
auth = (env.str('JIRA_USERNAME'), env.str('JIRA_API_TOKEN'))

# Get ticket details
response = requests.get(ticket_url, headers=headers, auth=auth)
ticket_data = response.json()

# Create a file within the "tickets" folder
output_filename = os.path.join("tickets", f"{ticket_id}.json")

# Write ticket JSON data to the file
with open(output_filename, "w") as output_file:
    json.dump(ticket_data, output_file, indent=4)

print(f"JSON data saved to {output_filename}")
