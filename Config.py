import configparser

class Config:
    def __init__(self):
        self.config_parser = configparser.RawConfigParser()


    def read_config(self):
        self.config_parser.read('.jsoniq.cfg')
        config = dict(self.config_parser.items('CONNECTION_DETAILS'))
        return config

config = Config()
config_data = config.read_config()