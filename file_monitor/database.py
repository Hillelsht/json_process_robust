import asyncpg
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging to display timestamps, log level, and messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    def __init__(self):
        # Initialize the database configuration using environment variables
        self.db_config = {
            'user': os.getenv('DB_USER', 'DB_USER'),
            'password': os.getenv('DB_PASSWORD', 'DB_PASSWORD'),
            'database': os.getenv('DB_NAME', 'DB_NAME'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }

    async def create_database(self):
        """
        Connects to the PostgreSQL server and creates the database if it does not exist.
        """
        try:
            # Connect to the default 'postgres' database to check for and create the target database
            conn = await asyncpg.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                database='postgres',  # Connect to the default database
                host=self.db_config['host'],
                port=self.db_config['port']
            )
            # Check if the target database exists
            query = f"SELECT 1 FROM pg_database WHERE datname = '{self.db_config['database']}'"
            result = await conn.fetch(query)
            if not result:
                # Create the target database if it does not exist
                await conn.execute(f'CREATE DATABASE {self.db_config["database"]}')
                logging.info(f"Database '{self.db_config['database']}' created successfully.")
            else:
                logging.info(f"Database '{self.db_config['database']}' already exists.")
            await conn.close()
        except Exception as e:
            logging.error("Error creating database: %s", e)
            raise

    async def connect(self):
        """
        Ensures the database exists and establishes a connection pool for the application.
        """
        await self.create_database()  # Ensure the database exists before connecting
        self.pool = await asyncpg.create_pool(**self.db_config)  # Create a connection pool
        await self.create_tables()  # Create the necessary tables in the database

    async def create_tables(self):
        """
        Creates the required tables in the database if they do not exist.
        """
        try:
            async with self.pool.acquire() as conn:
                # Create 'objects_detection' table
                await conn.execute('''CREATE TABLE IF NOT EXISTS objects_detection (
                                        vehicle_id TEXT,
                                        detection_time TEXT,  -- Store as TEXT
                                        object_type TEXT,
                                        object_value INTEGER
                                     )''')
                # Create 'vehicles_status' table
                await conn.execute('''CREATE TABLE IF NOT EXISTS vehicles_status (
                                        vehicle_id TEXT,
                                        report_time TEXT,  -- Store as TEXT
                                        status TEXT
                                     )''')
                # Create indexes for performance improvement
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_vehicle_id ON objects_detection(vehicle_id)')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_detection_time ON objects_detection(detection_time)')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_vehicle_status_id ON vehicles_status(vehicle_id)')
                await conn.execute('CREATE INDEX IF NOT EXISTS idx_report_time ON vehicles_status(report_time)')
        except Exception as e:
            logging.error("Error creating tables: %s", e)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def insert_objects_detection(self, data):
        """
        Inserts objects detection data into the database in batches.
        Uses retry mechanism to handle transient errors.
        """
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.executemany('''INSERT INTO objects_detection 
                                               (vehicle_id, detection_time, object_type, object_value)
                                               VALUES ($1, $2, $3, $4)''', data)
        except Exception as e:
            logging.error("Error inserting objects detection data: %s", e)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def insert_vehicle_status(self, data):
        """
        Inserts vehicle status data into the database in batches.
        Uses retry mechanism to handle transient errors.
        """
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.executemany('''INSERT INTO vehicles_status 
                                               (vehicle_id, report_time, status)
                                               VALUES ($1, $2, $3)''', data)
        except Exception as e:
            logging.error("Error inserting vehicle status data: %s", e)
            raise
