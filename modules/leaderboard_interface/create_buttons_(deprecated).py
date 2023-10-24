


class RowView(View):
    def __init__(self, buttons, filter_value):
        super().__init__()
        for button in buttons.values():
            self.add_item(MyButton(button, filter_value))

class MainView(View):
    def __init__(self, buttons):
        super().__init__()
        for button in buttons:
            self.add_item(button)


    def create_buttons(self, values):
        def spacer_button():
            spacer_button = {
                "custom_id": str(uuid.uuid4()),
                "label": "_"

            }
            return spacer_button
        buttons_type = [
            {
                str(uuid.uuid4()) : spacer_button(),
                "today" : {
                    "custom_id": "today",
                    "emoji": "📅",
                    "label": "today.........."
                },
                "this_week" : {
                    "custom_id": "this_week",
                    "emoji": "📆",
                    "label": "this week..."
                },
                "this_month": {
                    "custom_id": "this_month",
                    "emoji": "🗓️",
                    "label": "this month"
                },
                str(uuid.uuid4()) : spacer_button(),
            },
            {
                str(uuid.uuid4()): spacer_button(),
                "study": {
                    "custom_id": "study",
                    "emoji": "📖",
                    "label": "study only.."
                },
                "all_activities": {
                    "custom_id": "all_activities",
                    "emoji": "👣",
                    "label": "all activities "
                },
                str(uuid.uuid4()): spacer_button(),
                str(uuid.uuid4()): spacer_button(),

            },
            {
                str(uuid.uuid4()): spacer_button(),
                "both_only": {
                "custom_id": "both_only",
                "emoji": "🔥",
                "label": "cam and ss"
            },
            "exclude_no_cam": {
                "custom_id": "exclude_no_cam",
                "emoji": "📷",
                "label": "cam or ss....."
            },
            "all_types": {
                "custom_id": "all_types",
                "emoji": "☎️",
                "label": "no cam"
            },
            str(uuid.uuid4()): spacer_button(),

            },
        ]

        # Then in your main code:
        buttons = []
        for i, button_row in enumerate(buttons_type):
            for button in button_row.values():
                buttons.append(MyButton(self, button, values[i], i))
        main_view = MainView(buttons)
        return main_view
