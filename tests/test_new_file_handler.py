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
    mock_data = '{"objects_detection_events":[{"vehicle_id":"ebab5f787798416fb2b8afc1340d7a4e","detection_time":"2022-06-05T21:02:34.546Z","object_type":"pedestrians","object_value":3},{"vehicle_id":"ebab5f787798416fb2b8afc1340d7a4e","detection_time":"2022-06-05T21:05:20.590Z","object_type":"cars","object_value":4},{"vehicle_id":"ebab5f787798416fb2b8afc1340d7a4e","detection_time":"2022-06-05T21:11:35.567Z","object_type":"trucks","object_value":4}]}'
    mocker.patch('aiofiles.open', mocker.mock_open(read_data=mock_data))
    mocker.patch.object(db, 'insert_objects_detection', return_value=None)
    
    await handler.process_objects_detection('objects_detection_20240703T210234.json')
    db.insert_objects_detection.assert_called_once()

@pytest.mark.asyncio
async def test_process_vehicles_status(db, mocker):
    handler = NewFileHandler(db)
    mock_data = '{"vehicle_status":[{"vehicle_id":"ebab5f787798416fb2b8afc1340d7a4e","report_time":"2022-05-05T22:02:34.546Z","status":"driving"},{"vehicle_id":"ebae3f787798416fb2b8afc1340d7a6d","report_time":"2022-05-06T00:02:34.546Z","status":"accident"},{"vehicle_id":"qbae3f787798416fb2b8afc1340ddf19","report_time":"2022-05-09T00:02:34.546Z","status":"parking"}]}'
    mocker.patch('aiofiles.open', mocker.mock_open(read_data=mock_data))
    mocker.patch.object(db, 'insert_vehicle_status', return_value=None)
    
    await handler.process_vehicles_status('vehicles_status_20240703T220234.json')
    db.insert_vehicle_status.assert_called_once()
