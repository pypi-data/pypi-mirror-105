#!/usr/bin/env python3

from configparser import ConfigParser
import os

"""
This handles all of our config needs for UNGI
"""



def config(section, option, filename):
    """
    Used to load the config and parse its values
    """
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        val = parser.get(section, option)
        return val

def list_index(section, filename):
    """
    used to list es indexes from ini file
    """
    parser = ConfigParser()
    parser.read(filename)
    index_list = []
    for x in parser[f"{section}"]:
        index_list.append(parser.get(f"{section}", x))
    return index_list

def auto_load(str_in=None):
    """
    used to load the config. the str_in is to be used for the path
    if it is None (when the user does not pass a argument) it will
    load the path from the env var UNGI_CONFIG
    """
    if str_in:
        return str_in
    else:
        config_path = os.environ["UNGI_CONFIG"]
        return config_path

class UngiConfig:
    """
    A Common config class used for bots and ungi cli tools
    only input is a path to the ini file
    """
    def __init__(self, path):
        self.config_path = path
        self.es_host = config("ES", "host", self.config_path) # elasticsearch
        self.db_path = config("DB", "path", self.config_path) # loot db path
        self.sql_script = config("DB", "script", self.config_path) #sql script
        self.discord = config("INDEX", "discord", self.config_path) #discord index
        self.reddit = config("INDEX", "reddit", self.config_path) #reddit index
        self.telegram = config("INDEX", "telegram", self.config_path) #telegram index
        self.loot = config("INDEX", "loot", self.config_path) # loot index
        self.reddit_client_id = config("REDDIT", "client_id", self.config_path)
        self.reddit_client_secret = config("REDDIT", "client_secret", self.config_path)
        self.reddit_client_username = config("REDDIT", "username", self.config_path)
        self.reddit_client_password = config("REDDIT", "password", self.config_path)
        self.reddit_client_user_agent = config("REDDIT", "user_agent", self.config_path)
        self.telegram_api_id = int(config("TELEGRAM", "api_id", self.config_path))
        self.telegram_api_hash = config("TELEGRAM", "api_hash", self.config_path)
        self.telegram_session = config("TELEGRAM", "session_file", self.config_path)
        self.telegram_media = config("TELEGRAM", "media", self.config_path)
        self.telegram_store_media = config("TELEGRAM", "store_media", self.config_path)
        self.timezone = config("TIME", "timezone", self.config_path)
        self.twitter = config("INDEX", "twitter", self.config_path)
        if self.telegram_store_media == "True" or self.telegram_store_media == "true":
            self.telegram_store_media = True
        else:
            self.telegram_store_media = False
