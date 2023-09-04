import webbrowser
from jira import JIRA
import argparse
from tabulate import tabulate
from environ import Env

# Initialize the environment variable reader
env = Env()
env.read_env()

# Jira server URL, username, and API token (or password)
JIRA_SERVER = env.str("JIRA_SERVER")
JIRA_USERNAME = env.str("JIRA_USERNAME")
JIRA_API_TOKEN = env.str("JIRA_API_TOKEN")

# Parse command line arguments
parser = argparse.ArgumentParser(description="Fetch and process closed Jira tickets")
parser.add_argument("--open-links", action="store_true", help="Open ticket links in browser")
args = parser.parse_args()

# Connect to Jira using provided credentials
jira = JIRA(JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

# Fetch the active sprint for your project (assuming you know the board ID)
board_id = 1  # Read from environment variable
active_sprint = jira.sprints(board_id, state='active')[0]

# Get the list of issues (tickets) in the active sprint
sprint_issues = jira.search_issues(f'sprint={active_sprint.id}', maxResults=False)

# Filter closed issues
closed_issues = [issue for issue in sprint_issues if issue.fields.status.name == 'Closed']

# Create a table of closed issues with PR to staging info
table_data = []
for issue in closed_issues:
    ticket_number = issue.key
    ticket_summary = issue.fields.summary
    ticket_link = f"{JIRA_SERVER}/browse/{ticket_number}"
    
    # Open ticket link in browser if --open-in-browser is True
    if args.open_links:
        print(f"Opening new tab for {ticket_number} ({ticket_link})")
        webbrowser.open_new_tab(ticket_link)
    
    # Ask about PR to staging
    pr_to_staging = input(f"Does ticket [{ticket_number}]({ticket_link}) have a PR to staging? (Yes/No): ").strip().lower()
    
    if pr_to_staging in ['yes', 'y']:
        pr_status = "Yes"
        merge_status = input(f"Has the PR for [{ticket_number}]({ticket_link}) been merged? (Yes/No): ").strip().lower()
        if merge_status in ['yes', 'y']:
            merge_reason = ""
        else:
            merge_reason = input("Please provide the reason for not being merged: ").strip() or "Pending"
    elif pr_to_staging in ['no', 'n']:
        merge_status = ""
        merge_reason = input("Please provide remarks: ").strip() or "No PR to staging"
        pr_status = "No"
    else:
        print("Invalid input. Assuming No PR to staging.")
        pr_status = "No"
        merge_status = ""
        merge_reason = "Invalid input"
    
    table_data.append([f"[{ticket_number}]({ticket_link})", ticket_summary, pr_status, merge_status.capitalize(), merge_reason])

# Print the table using tabulate
table_headers = ["Ticket Number/Id", "Ticket Summary", "PR to Staging", "Merge Status", "Merge Reason"]
table = tabulate(table_data, headers=table_headers, tablefmt="github")
print(table)

# Save the table to a file
with open("closed-tickets-summary.txt", "w") as file:
    file.write(table)

print(f"Total closed issues in sprint {active_sprint.name}: {len(closed_issues)}")
