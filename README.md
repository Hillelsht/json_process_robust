
# Vehicle Status and Detection Processing

## Overview
This project monitors a directory for new JSON files containing vehicle status and detection events, and updates a PostgreSQL database with the information. The JSON files are processed asynchronously to handle high load and large file sizes efficiently.

## Requirements
- Python 3.11.2
- PostgreSQL
- `watchdog` library
- `asyncpg` library
- `tenacity` library
- `ijson` library
- `aiofiles` library
- `python-dotenv` library
- `pytest` library


## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Hillelsht/vehicle-data-pipeline-robust.git
    cd vehicle-data-pipeline-robust
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Create and Configure the .env File**:
    Create a `.env` file in the project root with the following content:
    ```ini
    DB_NAME=vehicles_db
    DB_USER=USERNAME
    DB_PASSWORD=PASSWORD
    DB_HOST=localhost
    DB_PORT=5432
    DIRECTORY_TO_WATCH=data/
    ```
4. **Install PostgreSQL**:
    ```bash
    # Ubuntu:
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    # Windows https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
    # Edit the PATH Environment Variable
    ```

4. **Configure PostgreSQL**:
    - Ensure PostgreSQL is installed and running.
    - Create a PostgreSQL SUPERUSER
      ```bash
      CREATE USER hillels WITH PASSWORD 'hillels' SUPERUSER;
      ```
    - The database will be created automatically if it does not exist.

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
- `data`
- `file_monitor/`
  - `__init__.py`
  - `file_monitor.py`
  - `new_file_handler.py`
  - `database.py`
- `tests/`
  - `__init__.py`
  - `test_database.py`
  - `test_file_monitor.py`
  - `test_new_file_handler.py`
- `main.py`
- `requirements.txt`
- `README.md`
- `DesignDocument.md`
- `.env`

## Contact
Hillel Shteyn 
hishtein@gmail.com
