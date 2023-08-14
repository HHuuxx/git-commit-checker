# Git Commit Checker

This Python script allows you to check if specific commit hashes are present in a given branch of a Git repository.

## Features

- Verify the existence of commit hashes in a designated branch.
- Support for checking against different branches (default: `main`).
- Displays results in a clear tabular format.

## Prerequisites

- Python 3.x
- Git (command-line tool)

## Usage

1. Clone or download this repository.

2. Open a terminal or command prompt and navigate to the directory containing the `main.py` script.

3. Run the script using the following command:
```bash
python main.py --repo `/path/to/repository` --branch branch_name
```

Replace `/path/to/repository` with the path to your Git repository, and `branch_name` with the desired branch (default: `main`).

Optional Arguments:

`--repo`: Repository directory path. If not provided, the current directory is used.

`--branch`: Branch to check against. If not specified, defaults to `main`. 

# Directory Structure
Ensure your directory structure matches the following:

```
  main_directory/
    ├── main.py
    ├── tickets/
    │   ├── ticket_123.txt
    │   ├── ticket_456.txt
    ├── commit_hashes.txt  # Optional file

```
For individual ticket files, create files like `ticket_123.txt` within the `tickets` folder, with commit hashes listed line by line.

# Output
The script generates a table with information about the specified commit hashes. It includes the commit hash, its corresponding commit message (limited to 50 characters), and whether it's in the designated branch.

# Examples
To check commit hashes in the `staging` branch of the repository located at `/path/to/repository`:

```bash
python main.py --repo /path/to/repository --branch staging
```

# Note

* Ensure your repository directory structure is set up correctly to avoid issues or errors.
* If the tickets folder is missing, the script searches for a commit_hashes.txt file in the same directory as main.py.
Make sure you have the necessary permissions to access repository files.