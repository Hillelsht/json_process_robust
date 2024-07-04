import logging
import ijson
import aiofiles
import asyncio
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, db, loop):
        self.db = db
        self.loop = loop

    def on_created(self, event):
        if not event.is_directory:
            self.loop.run_until_complete(self.process_file(event.src_path))

    async def process_file(self, file_path):
        if 'objects_detection' in file_path:
            await self.process_objects_detection(file_path)
        elif 'vehicles_status' in file_path:
            await self.process_vehicles_status(file_path)

    async def process_objects_detection(self, file_path):
        try:
            async with aiofiles.open(file_path, 'r') as file:
                objects = ijson.items(file, 'objects_detection_events.item')
                formatted_data = [(obj['vehicle_id'], obj['detection_time'], obj['object_type'], obj['object_value']) async for obj in objects]
                await self.db.insert_objects_detection(formatted_data)
        except (ijson.JSONError, KeyError) as e:
            logging.error("Error processing objects detection file %s: %s", file_path, e)
        except Exception as e:
            logging.error("Unexpected error processing objects detection file %s: %s", file_path, e)

    async def process_vehicles_status(self, file_path):
        try:
            async with aiofiles.open(file_path, 'r') as file:
                statuses = ijson.items(file, 'vehicle_status.item')
                formatted_data = [(status['vehicle_id'], status['report_time'], status['status']) async for status in statuses]
                await self.db.insert_vehicle_status(formatted_data)
        except (ijson.JSONError, KeyError) as e:
            logging.error("Error processing vehicles status file %s: %s", file_path, e)
        except Exception as e:
            logging.error("Unexpected error processing vehicles status file %s: %s", file_path, e)
