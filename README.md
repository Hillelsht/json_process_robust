# Vehicle Status and Detection Processing

## Overview
This project monitors a directory for new JSON files containing vehicle status and detection events, and updates a PostgreSQL database with the information.

## Requirements
- Python 3.x
- PostgreSQL

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/vehicle-status-detection.git
    cd vehicle-status-detection
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Database**:
    - Ensure PostgreSQL is installed and running.
    - Create a database named `vehicles_db`.
    - Update the database connection parameters in `database.py`:
      ```python
      self.conn = psycopg2.connect(dbname='vehicles_db', user='your_user', password='your_password', host='localhost', port='5432')
      ```

5. **Set the Directory to Watch**:
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