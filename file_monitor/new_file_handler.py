import logging
import ijson
import aiofiles
import asyncio
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BATCH_SIZE = 1000  # Adjust the batch size based on your memory and performance requirements

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, db, loop):
        self.db = db
        self.loop = loop  # Pass the running event loop from the main application

    def on_created(self, event):
        if not event.is_directory:
            # Schedule the coroutine on the running event loop
            self.loop.create_task(self.process_file(event.src_path))

    async def process_file(self, file_path):
        if 'objects_detection' in file_path:
            await self.process_objects_detection(file_path)
        elif 'vehicles_status' in file_path:
            await self.process_vehicles_status(file_path)

    async def process_objects_detection(self, file_path):
        try:
            async with aiofiles.open(file_path, 'r') as file:
                objects = ijson.items(file, 'objects_detection_events.item')
                batch = []
                async for obj in objects:
                    batch.append((obj['vehicle_id'], obj['detection_time'], obj['object_type'], obj['object_value']))
                    if len(batch) >= BATCH_SIZE:
                        await self.db.insert_objects_detection(batch)
                        batch = []
                if batch:
                    await self.db.insert_objects_detection(batch)
        except (ijson.JSONError, KeyError) as e:
            logging.error("Error processing objects detection file %s: %s", file_path, e)
        except Exception as e:
            logging.error("Unexpected error processing objects detection file %s: %s", file_path, e)

    async def process_vehicles_status(self, file_path):
        try:
            async with aiofiles.open(file_path, 'r') as file:
                statuses = ijson.items(file, 'vehicle_status.item')
                batch = []
                async for status in statuses:
                    batch.append((status['vehicle_id'], status['report_time'], status['status']))
                    if len(batch) >= BATCH_SIZE:
                        await self.db.insert_vehicle_status(batch)
                        batch = []
                if batch:
                    await self.db.insert_vehicle_status(batch)
        except (ijson.JSONError, KeyError) as e:
            logging.error("Error processing vehicles status file %s: %s", file_path, e)
        except Exception as e:
            logging.error("Unexpected error processing vehicles status file %s: %s", file_path, e)
