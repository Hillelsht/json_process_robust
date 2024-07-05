from file_monitor.file_monitor import FileMonitor
import logging
import logging.handlers
import asyncio
from dotenv import load_dotenv

# Load environment variables from a .env file into the application
load_dotenv()

# Configure logging to display timestamps, log level, and messages
# Configure logging to log to both console and a rotating file handler
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Log to console
                        logging.handlers.RotatingFileHandler('project_log.log', maxBytes=10485760, backupCount=5)  # Log to rotating file
                    ])

if __name__ == "__main__":
    # Create an instance of FileMonitor, which will handle the monitoring of the directory
    monitor = FileMonitor()
    
    # Get the current event loop
    loop = asyncio.get_event_loop()
    
    try:
        # Run the start method of the FileMonitor instance until it completes
        # This method initializes the database, sets up the event handler, and starts monitoring the directory
        loop.run_until_complete(monitor.start())
    except KeyboardInterrupt:
        # Handle the case when the user manually interrupts the program (e.g., by pressing Ctrl+C)
        logging.info("File monitoring stopped by user.")
    except Exception as e:
        # Log any unexpected exceptions that occur during the execution of the event loop
        logging.error("Unexpected error: %s", e)
    finally:
        # Ensure that all asynchronous generators are properly closed
        loop.run_until_complete(loop.shutdown_asyncgens())
        
        # Close the event loop
        loop.close()
