import pytest
import asyncio
import aiofiles
from watchdog.events import FileCreatedEvent
from file_monitor.new_file_handler import NewFileHandler
from unittest.mock import MagicMock

@pytest.fixture
def db(mocker):
    return mocker.Mock()

@pytest.mark.asyncio
async def test_process_objects_detection(db, mocker):
    handler = NewFileHandler(db)
    mock_data = '{"objects_detection_events":[{"vehicle_id":"vid1","detection_time":"2022-01-01T00:00:00Z","object_type":"car","object_value":1}]}'
    mocker.patch('aiofiles.open', mocker.mock_open(read_data=mock_data))
    mocker.patch.object(db, 'insert_objects_detection', return_value=None)
    
    await handler.process_objects_detection('dummy_path')
    db.insert_objects_detection.assert_called_once()

@pytest.mark.asyncio
async def test_process_vehicles_status(db, mocker):
    handler = NewFileHandler(db)
    mock_data = '{"vehicle_status":[{"vehicle_id":"vid1","report_time":"2022-01-01T00:00:00Z","status":"driving"}]}'
    mocker.patch('aiofiles.open', mocker.mock_open(read_data=mock_data))
    mocker.patch.object(db, 'insert_vehicle_status', return_value=None)
    
    await handler.process_vehicles_status('dummy_path')
    db.insert_vehicle_status.assert_called_once()
