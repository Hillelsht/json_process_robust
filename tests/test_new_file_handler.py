import pytest
import asyncio
import aiofiles
from watchdog.events import FileCreatedEvent
from file_monitor.new_file_handler import NewFileHandler
from unittest.mock import MagicMock

@pytest.fixture
def db(mocker):
    """
    Fixture to provide a mock database connection.
    """
    return mocker.Mock()

@pytest.fixture
def loop():
    """
    Fixture to provide the event loop.
    """
    return asyncio.get_event_loop()

@pytest.mark.asyncio
async def test_process_objects_detection(db, mocker, loop):
    """
    Test the process_objects_detection method to ensure objects detection data is processed and inserted correctly.
    """
    handler = NewFileHandler(db, loop)
    mock_data = '{"objects_detection_events":[{"vehicle_id":"vid1","detection_time":"2022-06-05T21:02:34.546Z","object_type":"car","object_value":1}]}'
    mocker.patch('aiofiles.open', mocker.mock_open(read_data=mock_data))
    mocker.patch.object(db, 'insert_objects_detection', return_value=None)
    
    await handler.process_objects_detection('objects_detection_20240703T210234.json')
    db.insert_objects_detection.assert_called_once()

@pytest.mark.asyncio
async def test_process_vehicles_status(db, mocker, loop):
    """
    Test the process_vehicles_status method to ensure vehicle status data is processed and inserted correctly.
    """
    handler = NewFileHandler(db, loop)
    mock_data = '{"vehicle_status":[{"vehicle_id":"vid1","report_time":"2022-05-05T22:02:34.546Z","status":"driving"}]}'
    mocker.patch('aiofiles.open', mocker.mock_open(read_data=mock_data))
    mocker.patch.object(db, 'insert_vehicle_status', return_value=None)
    
    await handler.process_vehicles_status('vehicles_status_20240703T220234.json')
    db.insert_vehicle_status.assert_called_once()
