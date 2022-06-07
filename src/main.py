#!/usr/bin/env python3

import os
import sys
import logging.config
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/..")
from src.lib.aws import send_message
from src.lib.db import get_db_session, get_clients

log = logging.getLogger(__name__)


def run():
    log.info("Starting scheduler")
    try:
        # Connect to the database
        session = get_db_session()
        clients = get_clients(session)
        for client in clients:
            log.info("Queuing user (%s)" % client.username)
            send_message(json.dumps(client.to_dict()["websites"]), username=client.username, email=client.email, notifications=client.notifications)
        # Close DB Connection
        session.close()

    except KeyboardInterrupt:
        log.info("Stopping service...")


if __name__ == "__main__":
    run()
