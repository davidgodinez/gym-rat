import unittest
from unittest.mock import MagicMock
from Central_070923 import user, weight, get_time, iothub_client_init, send_telemetry_from_pi

class TestCentralFunctions(unittest.TestCase):

    def test_user(self):
        # Test that the user function returns a string
        self.assertIsInstance(user(), str)

    def test_weight(self):
        # Test that the weight function returns an integer
        self.assertIsInstance(weight(), int)

    def test_get_time(self):
        # Test that the get_time function returns a string
        self.assertIsInstance(get_time(), str)

    def test_iothub_client_init(self):
        # Test that the iothub_client_init function returns an instance of IoTHubDeviceClient
        self.assertIsInstance(iothub_client_init(), IoTHubDeviceClient)

    def test_send_telemetry_from_pi(self):
        # Test that the send_telemetry_from_pi function sends a message
        new_messenger = MagicMock()
        telemetry_msg = {
            "gym_id": 1,
            "machine_id": 1,
            "user_id": "test_user",
            "rep_count": 10,
            "weight": 1,
            "reptime": "01/01/2022 12:00:00"
        }
        send_telemetry_from_pi(new_messenger, telemetry_msg)
        new_messenger.send_message.assert_called_once()