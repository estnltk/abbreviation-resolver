# -*- coding: UTF-8 -*-
import os
import logging.config

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Abbreviations webapp')
    parser.add_argument('-r', '--run', action='store_true', help='launch Flask built-in webserver')
    parser.add_argument('--log-config', metavar='<file.cfg>', action='store', help='read python logging configuration from the given .cfg file')
    args = parser.parse_args()
    if args.log_config is not None:
        logging.config.fileConfig(args.log_config)
    else:
        logging.basicConfig(level=logging.DEBUG)
    if args.run:
        from .main import app
        app.run(host=app.config['DEBUG_SERVER_HOST'], port=app.config['DEBUG_SERVER_PORT'])