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
- **Responsibility**: Connects to PostgreSQL, creates necessary tables, and performs insert or update operations.

### Database Schema

#### `objects_detection`
- `vehicle_id` (TEXT)
- `detection_time` (TIMESTAMP)
- `object_type` (TEXT)
- `object_value` (INTEGER)

#### `vehicles_status`
- `vehicle_id` (TEXT PRIMARY KEY)
- `report_time` (TIMESTAMP)
- `status` (TEXT)

### Design Choices

1. **Database**: PostgreSQL was chosen for its robustness, ACID compliance, and familiarity.
2. **Indexing**: Indexes were added to `vehicle_id` and timestamp columns to improve query performance.
3. **File Handling**: The `watchdog` library was used to monitor the directory for new files efficiently.

## Assumptions
- Each `vehicles_status` file contains the latest status, requiring updates to existing records.
- Files are named correctly as per the given format.

## Error Handling
- Errors during file processing or database operations are logged.
- Future improvements could include a retry mechanism for failed operations.

## Performance Considerations
- Batch inserts using `execute_values` to reduce transaction overhead.
- Indexes to optimize query performance.

## Future Enhancements
- Implement connection pooling to reuse database connections.
- Use asynchronous processing for better throughput.
- Add caching for frequently accessed data.

## Flow Chart

### File Processing Flow
                           +-----------------------+
                           |    Start Monitoring   |
                           +----------+------------+
                                      |
                                      v
                           +----------+------------+
                           |  File Created Event   |
                           +----------+------------+
                                      |
                                      v
                   +------------------+-------------------+
                   |                                      |
                   v                                      v
      +-------------+-------------+           +--------------+-----------+
      | Process Objects Detection |           |  Process Vehicles Status  |
      +-------------+-------------+           +--------------+-----------+
                   |                                      |
                   v                                      v
+-------------------+--------------------+ +----------------+------------------+
| Insert Detection Events into Database  | | Insert Vehicle Status in Database  |
+-------------------+--------------------+ +----------------+------------------+
                                          |
                                          v
                            +----------+------------+
                            | Continue Monitoring   |
                            +-----------------------+
