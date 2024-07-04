# Design Document for Vehicle Status and Detection Processing

## Overview
This document describes the design and architecture of the Vehicle Status and Detection Processing project.

## Architecture

### File Monitoring
- **Tool**: `watchdog`
- **Responsibility**: Monitors a specified directory for new JSON files and triggers processing when new files are detected.

### Event Handling
- **Class**: `NewFileHandler`
- **Responsibility**: Handles file creation events. Processes `objects_detection` and `vehicles_status` files by reading and parsing the JSON content, then updating the database.

### Database Interaction
- **Class**: `Database`
- **Responsibility**: Connects to PostgreSQL, ensures the database and tables exist, and performs insert operations.

### Database Schema

#### `objects_detection`
- `vehicle_id` (TEXT)
- `detection_time` (TEXT)  -- Stored as string
- `object_type` (TEXT)
- `object_value` (INTEGER)

#### `vehicles_status`
- `vehicle_id` (TEXT)
- `report_time` (TEXT)  -- Stored as string
- `status` (TEXT)

### Design Choices

1. **Database**: PostgreSQL was chosen for its robustness, ACID compliance, and familiarity.
2. **Indexing**: Indexes were added to `vehicle_id` and time columns to improve query performance.
3. **File Handling**: The `watchdog` library was used to monitor the directory for new files efficiently.
4. **Asynchronous Processing**: The `asyncpg`, `aiofiles`, and `ijson` libraries were used to handle large files and high loads efficiently.
5. **Retry Mechanism**: The `tenacity` library was used to implement retry logic for database operations.

## Assumptions
- Each `vehicles_status` file contains the latest status, requiring inserts for new records.
- Files are named correctly as per the given format.
- The date-time strings are stored as strings in the database.

## Error Handling
- Errors during file processing or database operations are logged.
- Retry logic with `tenacity` is implemented for database operations.

## Performance Considerations
- Asynchronous processing and streaming JSON parsing with `ijson` to handle large files.
- Indexes to optimize query performance.

## Future Enhancements
- Implement connection pooling to reuse database connections.
- Use more sophisticated caching for frequently accessed data.
- Introduce more granular error handling and reporting mechanisms.

## Flow Chart

## File Processing Flow

1. **Start Monitoring**
    - Initiate the file monitoring process in the specified directory.

2. **File Created Event**
    - Detect the creation of a new file in the monitored directory.

3. **Process File Based on Type**
    - If the file name contains "objects_detection":
        a. Read and parse the JSON content for objects detection events.
        b. Extract relevant data fields (vehicle_id, detection_time, object_type, object_value).
        c. Insert extracted data into the `objects_detection` table in the database.

    - If the file name contains "vehicles_status":
        a. Read and parse the JSON content for vehicle status events.
        b. Extract relevant data fields (vehicle_id, report_time, status).
        c. Insert extracted data into the `vehicles_status` table in the database.

4. **Continue Monitoring**
    - Continue monitoring the directory for new files.

                               +------------------------+
                               |    Start Monitoring    |
                               +------------------------+
                                          |
                                          v
                               +------------------------+
                               |   File Created Event   |
                               +------------------------+
                                          |
                                          v
                +-------------------------+-------------------------+
                |                                                   |
                v                                                   v
+-------------------------------+                     +-------------------------------+
|  Process Objects Detection    |                     |  Process Vehicles Status      |
+-------------------------------+                     +-------------------------------+
                |                                                   |
                v                                                   v
+-------------------------------+                     +-------------------------------+
| Insert Detection Events into  |                     | Insert Vehicle Status into    |
| Database                      |                     | Database                      |
+-------------------------------+                     +-------------------------------+
                                          |
                                          v
                               +------------------------+
                               | Continue Monitoring    |
                               +------------------------+


