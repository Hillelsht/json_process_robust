import pytest
import asyncio
from file_monitor.database import Database

@pytest.fixture
async def db():
    database = Database()
    await database.connect()
    yield database
    await database.conn.close()

@pytest.mark.asyncio
async def test_create_tables(db, mocker):
    mocker.patch.object(db, 'create_tables', return_value=None)
    await db.create_tables()
    db.create_tables.assert_called_once()

@pytest.mark.asyncio
async def test_insert_objects_detection(db, mocker):
    mock_data = [
        ('vehicle_id_1', '2022-01-01T00:00:00Z', 'pedestrian', 3),
        ('vehicle_id_2', '2022-01-01T01:00:00Z', 'car', 2),
    ]
    mocker.patch.object(db, 'insert_objects_detection', return_value=None)
    await db.insert_objects_detection(mock_data)
    db.insert_objects_detection.assert_called_once_with(mock_data)

@pytest.mark.asyncio
async def test_insert_vehicle_status(db, mocker):
    mock_data = [
        ('vehicle_id_1', '2022-01-01T00:00:00Z', 'driving'),
        ('vehicle_id_2', '2022-01-01T01:00:00Z', 'parked'),
    ]
    mocker.patch.object(db, 'insert_vehicle_status', return_value=None)
    await db.insert_vehicle_status(mock_data)
    db.insert_vehicle_status.assert_called_once_with(mock_data)
