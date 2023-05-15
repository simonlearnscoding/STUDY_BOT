from easy_pil import Canvas, Editor, Font, Text, font
from PIL import Image

def create_leaderboard_image(data):
    row_height = 40
    padding = 10
    width = 600
    height = padding + (row_height * len(data))
    
    canvas = Canvas(width, height)
    
    online_indicator = Image.new('RGBA', (10, 10), (0, 255, 0, 255))
    offline_indicator = Image.new('RGBA', (10, 10), (255, 0, 0, 255))

    font_path = font("arial.ttf")
    text_font = Font().load(font_path, 24)

    for index, row in enumerate(data):
        y_pos = padding + (index * row_height)

        # Nick
        canvas.text((padding, y_pos), Text().text(row['nick']).font(text_font))

        # Duration
        duration_text = f"{row['hours']}h {row['minutes']}m"
        canvas.text((width - padding - 100, y_pos), Text().text(duration_text).font(text_font))

        # Online status
        indicator = online_indicator if row['online'] else offline_indicator
        canvas.paste((width - padding - 40, y_pos + 5), indicator)

    return canvas.render()

# Example usage
