import os
import subprocess
from tabulate import tabulate
import textwrap
import argparse
import sys

# Check if the required libraries are installed
try:
    from tabulate import tabulate
except ImportError:
    print("Please install the 'tabulate' library using 'pip install tabulate'")
    sys.exit(1)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Check commit hashes in a specific branch")
parser.add_argument("--repo", help="Directory path of the repository")
parser.add_argument("--branch", help="Name of the branch to check against")
args = parser.parse_args()

# Get the repository directory from command-line argument or use the current directory
if args.repo:
    repo_directory = os.path.abspath(args.repo)
else:
    repo_directory = os.getcwd()

# Get the "tickets" directory within the repository
tickets_directory = os.path.join(repo_directory, "tickets")

# Get the project name from the repository directory name
project_name = os.path.basename(repo_directory)

# Specify the branch you want to check against (default to "main")
target_branch = args.branch if args.branch else "main"

# Create a list to store table rows
table = []

# Check if the "tickets" directory exists
if os.path.exists(tickets_directory):
    # Loop through ticket files
    for ticket_file in os.listdir(tickets_directory):
        try:
            if ticket_file.endswith(".txt"):
                ticket_number = os.path.splitext(ticket_file)[0]

                # Read commit hashes from the ticket's file
                ticket_file_path = os.path.join(tickets_directory, ticket_file)
                with open(ticket_file_path, "r") as f:
                    commit_hashes = [line.strip() for line in f]

                # Append a row for the ticket number
                table.append([f"Ticket {ticket_number}", "", "", ""])

                # Loop through the provided commit hashes
                for commit_hash in commit_hashes:
                    try:
                        commit_message = subprocess.check_output(['git', 'log', '-n', '1', '--format=%s', commit_hash], cwd=repo_directory).decode().strip()
                        # Limit or wrap commit message to 50 characters
                        commit_message = textwrap.shorten(commit_message, width=50, placeholder="...")
                        findings = subprocess.call(['git', 'merge-base', '--is-ancestor', commit_hash, f'{target_branch}^{{commit}}'], cwd=repo_directory)
                        if findings == 0:
                            findings_text = "In branch"
                        else:
                            findings_text = "Not in branch"
                        table.append(["", commit_hash, commit_message, findings_text])
                    except subprocess.CalledProcessError:
                        table.append(["", commit_hash, "Invalid commit hash", "Invalid"])
        except Exception as e:
            print(f"Error processing {ticket_file}: {e}")
else:
    # Check if commit_hashes.txt exists in the same folder as main.py
    commit_hashes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "commit_hashes.txt")
    if os.path.exists(commit_hashes_file):
        # Read commit hashes from commit_hashes.txt
        with open(commit_hashes_file, "r") as f:
            commit_hashes = [line.strip() for line in f]

        # Loop through the provided commit hashes
        for commit_hash in commit_hashes:
            try:
                commit_message = subprocess.check_output(['git', 'log', '-n', '1', '--format=%s', commit_hash], cwd=repo_directory).decode().strip()
                # Limit or wrap commit message to 50 characters
                commit_message = textwrap.shorten(commit_message, width=50, placeholder="...")
                findings = subprocess.call(['git', 'merge-base', '--is-ancestor', commit_hash, f'{target_branch}^{{commit}}'], cwd=repo_directory)
                if findings == 0:
                    findings_text = "In branch"
                else:
                    findings_text = "Not in branch"
                table.append(["Commit Hashes", commit_hash, commit_message, findings_text])
            except subprocess.CalledProcessError:
                table.append(["Commit Hashes", commit_hash, "Invalid commit hash", "Invalid"])
    else:
        print("Error: No 'tickets' folder or 'commit_hashes.txt' found. Create the 'tickets' folder with ticket files or a 'commit_hashes.txt' file in the same directory as 'main.py'.")

# Add the project name and branch info as a separate table
info_table = [["Project Name:", project_name], ["Branch:", target_branch]]

# Print the project info table
print(tabulate(info_table, tablefmt="grid"))

# Print an empty line for separation
print()

# Print the table using tabulate
headers = ["Ticket number", "Commit Hash", "Commit Message", "Findings"]
print(tabulate(table, headers=headers, tablefmt="grid"))
