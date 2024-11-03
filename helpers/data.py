import json
import logging

file_path = "./data/data.json"
logger = logging.getLogger("CattoBotto.data")

class Data:
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.load()

    def load(self):
        try:
            logger.info("Opening data file")
            with open(file_path) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            logger.error("Data file not found, creating one")
            self.data = {
                "version": 1,
                "queues": [],
            }
            self.save()

    def save(self):
        with open(file_path, 'w') as f:
            json.dump(self.data, f)