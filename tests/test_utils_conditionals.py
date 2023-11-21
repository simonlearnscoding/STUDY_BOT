import pytest
from unittest.mock import MagicMock, patch  # Import patch here
import modules.session_tracking.activities as act
from Cogs.VC_events import VCEvent
from utils.Conditionals import *


# import modules.session_tracking.activities as act


def test_user_changed_type_of_tracking():
    # Mock the VCEvent with different before and after states
    mock_event = MagicMock(spec=VCEvent)
    mock_event.before = MagicMock()
    mock_event.after = MagicMock()
