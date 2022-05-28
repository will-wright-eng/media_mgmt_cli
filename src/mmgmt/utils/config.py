"""
media management CLI - config setup
- export environment varibles
- setup dot directory at $HOME
- grab configs from AWS secrets
- os.environ.get("HOME", "Does not exist")
- use builtin python configparser "import configparser"

- add note to environment variable calls --> "environment variable {} not found, run `mmgmt configure` to setup"

`mmgmt configure`
- check environment variables
- check for .mmgmt dorectory in HOME --> .mmgmt/config
- mkdir $HOME/.mmgmt
- touch $HOME/.mmgmt/config

# what to inlcude in config file (store as yaml)
export AWS_BUCKET=media-backup-files
export AWS_BUCKET_PATH=media_uploads
export LOCAL_MEDIA_DIR=/Users/willwright/media/
export AWS_MEDIA_BUCKET=media-backup-files

AWS info
- aws bucket

"""

import os
import configparser
from pathlib import Path

class ConfigHandler:
    def __init__():
        self.home_path = os.environ.get("HOME", None)
        self.config_path = os.path.join(home_path,'.mmgmt','config')

        self.config = configparser.ConfigParser()
        if os.path.isfile(path)
            self.config.read(config_path)

    def export_configs(self):
        # export configs as environment variables
        x = self.config['test1']
        for key in x:
            print(key, x.get(key))
            os.environ[key.upper()] = x.get(key)   

    def write_config_file(self):
        # rewrite config file
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def create_file_and_dir(self):
        try:
            os.mkdir(os.path.join(self.home_path,'.mmgmt'))
        except FileExistsError as e:
            print(e)

        Path(self.config_path).touch()

    def config_file_input(config_dict: dict, section: str = "DEFAULT"):
        """
        example:
        config['DEFAULT'] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                      'CompressionLevel': '8',}
        """
        self.config[section] = config_dict
        