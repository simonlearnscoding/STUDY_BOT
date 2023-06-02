import pytest
import asynctest
from asynctest.mock import CoroutineMock
from cogs.time_passed import checkTime
update = checkTime()
import datetime
import io
import sys
import contextlib




import pytest
import asyncio
from unittest.mock import patch, AsyncMock

from cogs.time_passed import checkTime

@pytest.mark.asyncio
async def test_update_switch():
    message = '_start_of_day'
    timeStamp = '2023-06-02T12:34:56Z'
    switchName = 'day'
    data = {'switch': timeStamp}
    where = {"name": switchName}

    # Instantiate the class
    instance = checkTime()

    # Test when update is successful
    with patch('bases.connector.create_query', new_callable=AsyncMock) as mock_create_query:
        mock_create_query.return_value = 'Update successful'
        result = await instance.update_switch(message, timeStamp)
        mock_create_query.assert_called_with("switch", "update_many", where=where, data=data)
        assert result == 'Update successful'

    # Test when no entries found and a new entry is created
    with patch('bases.connector.create_query', new_callable=AsyncMock) as mock_create_query:
        mock_create_query.side_effect = [Exception('No entries found'), 'Create successful']
        result = await instance.update_switch(message, timeStamp)
        mock_create_query.assert_called_with("switch", "create", data=data)
        assert result == 'Create successful'