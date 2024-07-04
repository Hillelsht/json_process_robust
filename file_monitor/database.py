import asyncpg
import logging
from aioretry import retry
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    def __init__(self):
        self.db_config = {
            'user': os.getenv('DB_USER', 'your_user'),
            'password': os.getenv('DB_PASSWORD', 'your_password'),
            'database': os.getenv('DB_NAME', 'vehicles_db'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }

    async def connect(self):
        self.conn = await asyncpg.connect(**self.db_config)
        await self.create_tables()

    async def create_tables(self):
        try:
            await self.conn.execute('''CREATE TABLE IF NOT EXISTS objects_detection (
                                        vehicle_id TEXT,
                                        detection_time TIMESTAMP,
                                        object_type TEXT,
                                        object_value INTEGER
                                     )''')
            await self.conn.execute('''CREATE TABLE IF NOT EXISTS vehicles_status (
                                        vehicle_id TEXT,
                                        report_time TIMESTAMP,
                                        status TEXT
                                     )''')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_vehicle_id ON objects_detection(vehicle_id)')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_detection_time ON objects_detection(detection_time)')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_vehicle_status_id ON vehicles_status(vehicle_id)')
            await self.conn.execute('CREATE INDEX IF NOT EXISTS idx_report_time ON vehicles_status(report_time)')
        except Exception as e:
            logging.error("Error creating tables: %s", e)
            raise

    @retry(attempts=3, delay=2)
    async def insert_objects_detection(self, data):
        try:
            async with self.conn.transaction():
                await self.conn.executemany('''INSERT INTO objects_detection 
                                               (vehicle_id, detection_time, object_type, object_value)
                                               VALUES ($1, $2, $3, $4)''', data)
        except Exception as e:
            logging.error("Error inserting objects detection data: %s", e)
            raise

    @retry(attempts=3, delay=2)
    async def insert_vehicle_status(self, data):
        try:
            async with self.conn.transaction():
                await self.conn.executemany('''INSERT INTO vehicles_status 
                                               (vehicle_id, report_time, status)
                                               VALUES ($1, $2, $3)''', data)
        except Exception as e:
            logging.error("Error inserting vehicle status data: %s", e)
            raise

