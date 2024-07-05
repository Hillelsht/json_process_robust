from watchdog.observers import Observer
from .new_file_handler import NewFileHandler
from .database import Database
import logging
import asyncio
import os

# Configure logging to display timestamps, log level, and messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileMonitor:
    def __init__(self):
        """
        Initialize the FileMonitor with the directory to watch and the event loop.
        """
        # Get the directory to watch from environment variables or use a default value
        self.directory_to_watch = os.getenv('DIRECTORY_TO_WATCH', '/data')
        # Get the running event loop
        self.loop = asyncio.get_event_loop()

    async def start(self):
        """
        Start monitoring the directory for new files and process them.
        """
        # Initialize the Database instance and connect to the database
        self.db = Database()
        await self.db.connect()
        
        # Initialize the event handler with the database and event loop
        self.event_handler = NewFileHandler(self.db, self.loop)
        
        # Initialize the Observer to monitor the directory
        self.observer = Observer()
        
        # Schedule the event handler to monitor the specified directory
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=False)
        
        # Start the Observer
        self.observer.start()
        logging.info("Started monitoring directory: %s", self.directory_to_watch)
        
        try:
            while True:
                # Keep the event loop running
                await asyncio.sleep(1)
        except Exception as e:
            logging.error("Error during file monitoring: %s", e)
        finally:
            # Stop the Observer and wait for it to join
            self.observer.stop()
            self.observer.join()
            logging.info("Stopped monitoring directory: %s", self.directory_to_watch)
