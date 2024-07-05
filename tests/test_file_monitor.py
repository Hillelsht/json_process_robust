import pytest
from file_monitor.file_monitor import FileMonitor
from unittest.mock import patch, MagicMock
import os

@pytest.fixture
def file_monitor(mocker):
    """
    Fixture to provide a FileMonitor instance with a mock event loop.
    """
    mocker.patch('file_monitor.file_monitor.Database')
    monitor = FileMonitor()
    return monitor

def test_initialization(file_monitor):
    """
    Test the initialization of the FileMonitor instance.
    """
    assert file_monitor.directory_to_watch == '/path/to/watch'

@pytest.mark.asyncio
async def test_start(file_monitor, mocker):
    """
    Test the start method of the FileMonitor instance.
    """
    mocker.patch.object(file_monitor, 'start', return_value=None)
    await file_monitor.start()
    file_monitor.start.assert_called_once()
