import unittest

from bases.event_manager import EventManager


class MockSubscriber:
    def event_one(self, data):
        self.event_one_data = data

    def event_two(self, data):
        self.event_two_data = data


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.subscriber = MockSubscriber()
        self.event_manager.subscribe(self.subscriber)

    def test_publish_event_one(self):
        test_data = "Test data for event_one"
        self.event_manager.publish("event_one", test_data)
        self.assertEqual(self.subscriber.event_one_data, test_data)

    def test_publish_event_two(self):
        test_data = "Test data for event_two"
        self.event_manager.publish("event_two", test_data)
        self.assertEqual(self.subscriber.event_two_data, test_data)


if __name__ == "__main__":
    unittest.main()
