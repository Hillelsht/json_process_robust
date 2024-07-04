# Vehicle Status and Detection Processing

## Overview
This project monitors a directory for new JSON files containing vehicle status and detection events, and updates a PostgreSQL database with the information.

## Requirements
- Python 3.11.2
- PostgreSQL

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Hillelsht/json_process_robust.git
    cd json_process_robust
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv env_json_robust
    source env_json_robust/bin/activate  # On Windows, use `env_json_robust\Scripts\Activate.ps1`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Install DataBase**:
    ```bash
    # Ubuntu:
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    # Windows https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
    # Edit the PATH Environment Variable
    ```

5. **Configure Database**:
    - Ensure PostgreSQL is installed and running.
    - Create a user
      ```bash
      CREATE USER hillels WITH PASSWORD 'hillels' SUPERUSER;
      ```
    - The database will be created within the Database class

6. **Set the Directory to Watch**:
    - Set the `directory_to_watch` variable in `main.py` to the directory where JSON files will be placed.

## Running the Project

1. **Navigate to the project directory**:
    ```bash
    cd /path/to/project_root
    ```

2. **Run the script**:
    ```bash
    python main.py
    ```

## Project Structure

- `file_monitor/`
  - `__init__.py`
  - `file_monitor.py`
  - `new_file_handler.py`
  - `database.py`
- `main.py`
- `requirements.txt`
- `README.md`
- `DesignDocument.md`

## Contact

Hillel Shteyn 
hishtein@gmail.com