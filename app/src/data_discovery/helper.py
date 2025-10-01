import json
import os
class Comm_helper:
    def __init__(self):
        self.data_path = "apollo_mock_data.json"

    def load_config(self):
        config = json.load(open(self.data_path))
        return config
