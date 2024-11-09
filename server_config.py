'''to load config.json and return a GDTServerConfig object'''

import json
import os
import re

class _ConfigKeys:
    '''keys in config.json'''

    DBLINK = "dblink"
    HOST = "host"
    PORT = "port"
    DEBUG = "debug",
    LOGFOLDER = "log_folder"

class _ConfigUtils:

    def is_valid_mongodb_uri(uri: str) -> bool:
        # Regular expression to match MongoDB URI
        mongodb_uri_pattern = re.compile(
            r'^mongodb://'
            r'(?:(?P<username>[^:]+):(?P<password>[^@]+)@)?'  # Optional username:password@
            r'(?P<host>(?:\d{1,3}\.){3}\d{1,3})'              # IPv4 host
            r'(:(?P<port>\d+))?'                              # Optional port
            r'/?(?P<options>.*)?$'                            # Optional options/query string
        )
        
        # Check if the URI matches the pattern
        return mongodb_uri_pattern.match(uri)

    def is_valid_ipv4_addr(address: str) -> bool:
        # Regular expression to match valid IPv4 addresses
        ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
                                r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        
        return ipv4_pattern.match(address)
    
    def is_valid_port(port: int) -> bool:
        return 0 < port < 65536

class ServerConfig:
    '''server configs of game data tracker'''

    @staticmethod
    def load(path:str):
        '''given a json file path and read config from this path'''

        _invalid_config = ServerConfig("", 0, 0, True, False)
        if not os.path.exists(path) or not os.path.isfile(path):
            print("config file \"{path}\" not found")
            return _invalid_config
        
        '''load config from file'''
        with open(path, "r") as f:
            _src = json.load(f)
            if not _src:
                return _invalid_config
            
            _dblink = _src.get(_ConfigKeys.DBLINK)
            _host = _src.get(_ConfigKeys.HOST)
            _port = _src.get(_ConfigKeys.PORT)
            _debug = _src.get(_ConfigKeys.DEBUG)
            _log_folder = _src.get(_ConfigKeys.LOGFOLDER)
            
            if _dblink is None or not _ConfigUtils.is_valid_mongodb_uri(_dblink):
                print(_ConfigKeys.DBLINK + " not found in config file or invalid")
                return _invalid_config
            
            if _host is None or not _ConfigUtils.is_valid_ipv4_addr(_host):
                print(_ConfigKeys.HOST + " not found in config file or invalid")
                return _invalid_config
            
            if _port is None or not _ConfigUtils.is_valid_port(_port):
                print(_ConfigKeys.PORT + " not found in config file or invalid")
                return _invalid_config
            
            if _log_folder is None or not os.path.exists(_log_folder):
                print(_ConfigKeys.LOGFOLDER + " not found in config file or invalid")
                return _invalid_config
            
            if _debug is None:
                print(_ConfigKeys.DEBUG + " not found in config file")
                return _invalid_config
            
            return ServerConfig(_dblink, _host, _port, _debug, _log_folder, True)
        

    def __init__(self, dblink:str, server_host:int, server_port:int, debug:bool, log_folder:str, isvalid:bool):

        self.__dblink = dblink
        self.__host = server_host
        self.__port = server_port
        self.__debug = debug
        self.__is_valid = isvalid
        self.__log_folder = log_folder

    @property
    def debug_mode(self):
        '''if server is in debug mode'''

        return self.__debug
    
    @property
    def log_folder(self):
        '''get log folder'''

        return self.__log_folder

    @property
    def is_valid(self):
        '''if current config is invalid, then server won't run'''
        return self.__is_valid
    
    @property
    def server_addr(self):
        '''get server address'''

        return "http://{}:{}".format(self.__host, self.__port)
    
    @property
    def host(self):
        '''get server host'''

        return self.__host
    
    @property
    def port(self):
        '''get server port'''

        return self.__port
    
    
    @property
    def dblink(self):
        '''get database address of mongodb'''

        return self.__dblink
    

if __name__ == "__main__":

    _config = ServerConfig.load("./config.json")
    print(_config.is_valid)
    print(_config.server_addr)
    print(_config.dblink)