from file_monitor.file_monitor import FileMonitor
import logging
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    monitor = FileMonitor()
    try:
        monitor.loop.run_until_complete(monitor.start())
    except KeyboardInterrupt:
        logging.info("File monitoring stopped by user.")
    except Exception as e:
        logging.error("Unexpected error: %s", e)
