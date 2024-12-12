import configparser
import os
import importlib.resources

class Messages:
    def __init__(self):
        self.property_dict = {}

    def load_messages(self, lang):
        config = configparser.ConfigParser()

        # Access the resource file within the package
        with importlib.resources.open_text(
            __package__, f"messages_{lang}.properties"
        ) as file:
            config.read_file(file)

        for key, value in config.items("messages"):
            self.property_dict[key] = value

    def get(self, key):
        return self.property_dict.get(key)
