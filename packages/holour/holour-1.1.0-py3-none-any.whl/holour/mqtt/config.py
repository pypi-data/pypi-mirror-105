import os
import yaml
import logging


class MQTTConfig:

    def __init__(self,
                 client_id: str,
                 address: str = "localhost",
                 port: int = 1883,
                 keep_alive: int = 60,
                 prefix: str = '/'):
        self.address = address
        self.port = port
        self.keep_alive = keep_alive
        self.prefix = prefix.rstrip('/')
        self.client_id = client_id


def load_configuration(config_file: str, log: logging.Logger) -> dict:
    config = {}
    if not os.path.exists(config_file):
        log.error(f"The configuration file: {config_file} doesn't exist!")
        return config
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            log.info(f"Configuration: {config}")
        except yaml.YAMLError as e:
            log.error(e)
    return config
