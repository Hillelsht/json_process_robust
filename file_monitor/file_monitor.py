from watchdog.observers import Observer
from .new_file_handler import NewFileHandler
from .database import Database
import logging
import asyncio
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileMonitor:
    def __init__(self):
        self.directory_to_watch = os.getenv('DIRECTORY_TO_WATCH', '/path/to/watch')
        self.loop = asyncio.get_event_loop()

    async def start(self):
        self.db = Database()
        await self.db.connect()
        self.event_handler = NewFileHandler(self.db, self.loop)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=False)
        self.observer.start()
        logging.info("Started monitoring directory: %s", self.directory_to_watch)
        try:
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            logging.error("Error during file monitoring: %s", e)
        finally:
            self.observer.stop()
            self.observer.join()
            logging.info("Stopped monitoring directory: %s", self.directory_to_watch)
