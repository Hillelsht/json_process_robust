# Design Document for Vehicle Status and Detection Processing

## Overview
This document describes the design and architecture of the Vehicle Status and Detection Processing project, highlighting the key performance features implemented to handle high loads and large files efficiently.

## Architecture

### File Monitoring
- **Tool**: `watchdog`
- **Responsibility**: Monitors a specified directory for new JSON files and triggers processing when new files are detected.

### Event Handling
- **Class**: `NewFileHandler`
- **Responsibility**: Handles file creation events. Processes `objects_detection` and `vehicles_status` files by reading and parsing the JSON content incrementally, then updating the database in batches.

### Database Interaction
- **Class**: `Database`
- **Responsibility**: Connects to PostgreSQL using a connection pool, ensures the database and tables exist, and performs insert operations in batches.

### Performance Features

1. **Connection Pooling**:
    - **Library**: `asyncpg`
    - **Description**: Utilizes a connection pool to manage database connections efficiently, allowing multiple concurrent database operations without conflicts. This improves performance and prevents bottlenecks.

2. **Batch Processing**:
    - **Implementation**: Data is processed in batches of a configurable size before being inserted into the database.
    - **Benefit**: Reduces the memory footprint and improves database insertion performance, especially for large files.

3. **Incremental JSON Parsing**:
    - **Library**: `ijson`
    - **Description**: Parses JSON files incrementally, allowing the system to handle large JSON files without loading the entire file into memory.
    - **Benefit**: Efficient memory usage and the ability to process very large files.

4. **Asynchronous I/O**:
    - **Libraries**: `asyncio`, `aiofiles`
    - **Description**: Utilizes asynchronous I/O operations for file reading and database interactions.
    - **Benefit**: Non-blocking operations improve throughput and responsiveness, especially under high load conditions.

5. **Retry Mechanism**:
    - **Library**: `tenacity`
    - **Description**: Implements retry logic for database operations to handle transient errors.
    - **Benefit**: Increases robustness and reliability of database interactions.

## Database Schema

#### `objects_detection`
- `vehicle_id` (TEXT)
- `detection_time` (TEXT)
- `object_type` (TEXT)
- `object_value` (INTEGER)

#### `vehicles_status`
- `vehicle_id` (TEXT)
- `report_time` (TEXT)
- `status` (TEXT)

### Design Choices

1. **Database**: PostgreSQL was chosen for its robustness, ACID compliance.
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
- **Asynchronous Processing**: Non-blocking I/O operations using `asyncio` and `aiofiles`.
- **Batch Inserts**: Data is processed and inserted into the database in batches to optimize memory usage and performance.
- **Incremental JSON Parsing**: Uses `ijson` to parse JSON files incrementally, reducing memory usage.
- **Connection Pooling**: Manages multiple database connections concurrently with `asyncpg` to prevent conflicts and improve performance.
- **Retry Mechanism**: Ensures robustness and reliability with `tenacity`.

## Future Enhancements
- Implement more sophisticated caching for frequently accessed data.
- Introduce more granular error handling and reporting mechanisms.
- Database Sharding
- Database Index Optimization
- Data Partitioning
- Data Backup and Recovery Strategies
- Database Monitoring and Analytics
- Data Compression
- Distributed Processing: frameworks like Apache Spark

## Flow Chart

### File Processing Flow

```plaintext
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
                      +--------------+--------------+
                      |                             |
                      v                             v
+---------------------+----------------+ +---------------------+----------------+
|  Process Objects Detection File     | |  Process Vehicles Status File        |
+-------------------------------------+ +-------------------------------------+
| - Open file asynchronously          | | - Open file asynchronously          |
| - Parse JSON incrementally          | | - Parse JSON incrementally          |
| - Batch data                        | | - Batch data                        |
| - Insert batch into database        | | - Insert batch into database        |
+-------------------------------------+ +-------------------------------------+
                                     |
                                     v
                          +----------+------------+
                          |    Continue Monitoring |
                          +-----------------------+
