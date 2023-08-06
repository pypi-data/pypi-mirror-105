#!/usr/bin/env python

import logging
import logging.config
import os
import yaml
import sys
import argparse

DEFAULT_CONFIG    = os.getenv( 'CONFIGFILE', 'myapp.yaml' )
DEFAULT_LOGFILE   = os.getenv( 'LOGFILE', 'myapp.log' )

DEFAULT_LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOGLEVEL  = 'INFO'


def dictread( dictionary, key, default=None ):
    if dictionary is None:
        return default
    elif key in dictionary:
        return dictionary[key]
    else:
        return default


def forceread ( dictionary, key ):
    value = dictread(dictionary, key, None )
    if value is None:
        raise ValueError( f'Failed to read value {key} from configuration!')
    return value


class Config:

    c = None

    def __init__ ( self, filename=None ):

        if filename is None:
            filename = DEFAULT_CONFIG

        self.filename = filename
        self.readCommandLine()

        with open(self.filename) as source:
            self.config = yaml.load( source, Loader=yaml.FullLoader )

    def value ( self, key, default=None ):
        return dictread(self.config, key, default)

    @staticmethod
    def get ( key, default=None ):
        return dictread(Config.c.config, key, default)

    def readCommandLine ( self ):

        parser = argparse.ArgumentParser(description='Generic UpDryTwist Command Parser')
        parser.add_argument('--config', help='Path to configuration file', default=None)
        args = parser.parse_args()
        if 'config' in vars(args):
            fileName = vars(args)['config']
            if fileName is not None:
                self.filename = fileName


def getConfig () -> Config :
    return Config.c


def loadConfig ():
    try:
        Config.c = Config()
    except Exception as e:
        print( "Cannot load configuration from file {}: {}".format( DEFAULT_CONFIG, str(e)))
        sys.exit(2)


def initLogging ():

    loggingConfig = Config.get( 'Logging', None )
    incremental = dictread(loggingConfig, 'incremental', False )

    if incremental or not loggingConfig:
        # if the configuration is incremental, or missing, we set up most of the logging
        # in particular, we need to manage formatter and handler

        logFile   = Config.get( 'logfile',   DEFAULT_LOGFILE )
        logFormat = Config.get( 'logformat', DEFAULT_LOGFORMAT )
        logLevel  = Config.get( 'loglevel',  DEFAULT_LOGLEVEL )

        root = logging.getLogger()
        root.setLevel( logLevel )

        handler = logging.FileHandler( logFile )
        handler.setLevel( logLevel )
        handler.setFormatter( logging.Formatter(logFormat ))
        root.addHandler( handler )

    if loggingConfig:

        logging.config.dictConfig( loggingConfig )

        if not incremental:
            # if it's not incremental, then these are essentially overrides

            logFile   = Config.get( 'logfile',   None )
            logFormat = Config.get( 'logformat', None )
            logLevel  = Config.get( 'loglevel',  None )

            root = logging.getLogger()
            if logLevel:
                root.setLevel( logLevel )

            if logFile:
                handler = logging.FileHandler( logFile )
                if logLevel:
                    handler.setLevel( logLevel )
                if logFormat:
                    handler.setFormatter( logging.Formatter(logFormat ))
                root.addHandler( handler )

    """
    handler = logging.StreamHandler( sys.stdout )
    handler.setLevel( logLevel )
    handler.setFormatter( logging.Formatter( logFormat ))
    root.addHandler( handler )
    """


def initialize ():
    loadConfig()
    initLogging()
