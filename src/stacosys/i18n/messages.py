import configparser
import os


class Messages:
    def __init__(self):
        self.property_dict = {}

    def load_messages(self, lang):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'messages_' + lang + '.properties'))

        for key, value in config.items('messages'):
            self.property_dict[key] = value

    def get(self, key):
        return self.property_dict.get(key)
