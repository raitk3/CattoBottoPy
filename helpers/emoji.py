import json

class Emoji:
    def __init__(self) -> None:
        self.emoji = self.load_emoji()

    def load_emoji(self):
        json_read = {}
        with open("emoji.json") as f:
            json_read = json.load(f)
        return json_read["emoji"]