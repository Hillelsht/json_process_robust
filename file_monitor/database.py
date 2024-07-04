import asyncpg
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    def __init__(self):
        self.db_config = {
            'user': os.getenv('DB_USER', 'hillel'),
            'password': os.getenv('DB_PASSWORD', 'hillel'),
            'database': os.getenv('DB_NAME', 'vehicles_db'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }

    async def create_database(self):
        try:
            conn = await asyncpg.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                database='postgres',  # Connect to the default database
                host=self.db_config['host'],
                port=self.db_config['port']
            )
            query = f"SELECT 1 FROM pg_database WHERE datname = '{self.db_config['database']}'"
            result = await conn.fetch(query)
            if not result:
                await conn.execute(f'CREATE DATABASE {self.db_config["database"]}')
                logging.info(f"Database '{self.db_config['database']}' created successfully.")
            else:
                logging.info(f"Database '{self.db_config['database']}' already exists.")
            await conn.close()
        except Exception as e:
            logging.error("Error creating database: %s", e)
            raise

    async def connect(self):
        await self.create_database()  # Ensure the database exists before connecting
        self.conn = await asyncpg.connect(**self.db_config)
        await self.create_tables()

    async def create_tables(self):
        try:
            await self.conn.execute('''CREATE TABLE IF NOT EXISTS objects_detection (
                                        vehicle_id TEXT,
                                        detection_time TEXT, 
                                        object_type TEXT,
                                        object_value INTEGER
                                     )''')
            await self.conn.execute('''CREATE TABLE IF NOT EXISTS vehicles_status (
                                        vehicle_id TEXT,
                                        report_time TEXT, 
                                        status TEXT
                                     )''')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_vehicle_id ON objects_detection(vehicle_id)')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_detection_time ON objects_detection(detection_time)')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_vehicle_status_id ON vehicles_status(vehicle_id)')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_report_time ON vehicles_status(report_time)')
        except Exception as e:
            logging.error("Error creating tables: %s", e)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def insert_objects_detection(self, data):
        try:
            async with self.conn.transaction():
                await self.conn.executemany('''INSERT INTO objects_detection 
                                               (vehicle_id, detection_time, object_type, object_value)
                                               VALUES ($1, $2, $3, $4)''', data)
        except Exception as e:
            logging.error("Error inserting objects detection data: %s", e)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def insert_vehicle_status(self, data):
        try:
            async with self.conn.transaction():
                await self.conn.executemany('''INSERT INTO vehicles_status 
                                               (vehicle_id, report_time, status)
                                               VALUES ($1, $2, $3)''', data)
        except Exception as e:
            logging.error("Error inserting vehicle status data: %s", e)
            raise
