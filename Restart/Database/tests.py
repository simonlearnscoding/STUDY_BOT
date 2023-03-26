# test_my_module.py
import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock

from Restart.Database.connector import Database


def async_test(func):
    def wrapper(*args, **kwargs):
        coro = func(*args, **kwargs)
        asyncio.get_event_loop().run_until_complete(coro)

    return wrapper


class TestMyDatabaseClass(unittest.TestCase):
    @async_test
    async def test_createMomentLogEntry(self):
        # Create a MyDatabaseClass instance with a mocked database
        my_db = await Database.create()
        my_db.db = MagicMock()
        my_db.db.logsnow.create = AsyncMock()

        # Define test datauser
        time = "2023-03-25T12:00:00"
        type = "login"
        activity = "Logged in"
        member = {"id": 123456782022905678}

        # Call the createMomentLogEntry function
        created_user = await my_db.createMomentLogEntry(member, time, type, activity)

        # Test if the database create method was called with the correct data
        my_db.db.logsnow.create.assert_called_once_with(
            {
                "activity": activity,
                "timestamp": time,
                "type": type,
                "userId": member["id"],
            }
        )

        # Test if the created_user value is as expected
        self.assertEqual(created_user, my_db.db.logsnow.create.return_value)


if __name__ == "__main__":
    unittest.main()
