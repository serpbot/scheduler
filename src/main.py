#!/usr/bin/env python3

import os
import sys
import logging.config
import argparse
import configparser
import json

from src.lib.aws import send_message
from src.lib.db import get_db_session, get_clients

log = logging.getLogger(__name__)


def get_conf(env):
    """Get config object"""
    config = configparser.ConfigParser()
    basedir = os.path.abspath(os.path.dirname(__file__))
    if env == "prod":
        config.read(basedir + "/conf/prod.ini")
    else:
        config.read(basedir + "/conf/dev.ini")
    return config


def get_env():
    """Get environment to run in"""
    parser = argparse.ArgumentParser(description="Serpbot backend.")
    parser.add_argument("-e", "--env", default="dev",
                        help="select an environment to launch in (dev, prod)")
    args = parser.parse_args()
    if args.env.lower() not in ["dev", "prod"]:
        log.error("Invalid environment selected")
        sys.exit(1)
    return args.env.lower()


def run(env):
    log.info("Starting in %s mode", env)
    conf = get_conf(env)
    try:
        # Connect to the database
        session = get_db_session(conf)
        clients = get_clients(session)
        for client in clients:
            log.info("Queuing user (%s)" % client.username)
            send_message(json.dumps(client.to_dict()["websites"]), conf["sqs"]["name"], conf["sqs"]["region"], username=client.username, email=client.email)
        # Close DB Connection
        session.close()

    except KeyboardInterrupt:
        log.info("Stopping service...")


if __name__ == "__main__":
    run(get_env())
