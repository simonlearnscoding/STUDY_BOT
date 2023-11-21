# Get the parent directory

# Add the parent directory to sys.path
# Replace '' with the actual module name
from utils.Conditionals import user_changed_type_of_tracking
from unittest.mock import Mock, patch
import unittest
from Cogs.VC_events import VCEvent

from modules.session_tracking import activities as act



class TestUserChangedTypeOfTracking(unittest.TestCase):

    def test_user_changed_type_of_tracking(self):
        mock_member = Mock()
        mock_before_voice_state = Mock()
        mock_after_voice_state = Mock()

        mock_before_voice_state.channel.id = 'Channel1'
        mock_after_voice_state.channel.id = 'Channel2'

        # Mock the getActivity and getActivityType functions
        with patch('act.getActivityType') as mock_get_activity_type, \
                patch('act.getActivity') as mock_get_activity:

            mock_get_activity_type.side_effect = lambda vs: 'ActivityType1' if vs.channel.id == 'Channel1' else 'ActivityType2'
            mock_get_activity.side_effect = lambda vs: 'Activity1' if vs.channel.id == 'Channel1' else 'Activity2'

            # Create a VCEvent instance
            vc_event = VCEvent(
                mock_member, mock_before_voice_state, mock_after_voice_state)

            # Test the function
            result = user_changed_type_of_tracking(vc_event)

            # Assert the result
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
