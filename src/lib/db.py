#!/usr/bin/env python3
"""
This module empasses various functions used to query the database
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.model.orm import base, Client

log = logging.getLogger(__name__)


def get_db_session(conf):
    """Get db session"""
    engine = create_engine("mysql://%s:%s@%s/%s" % (conf["db"]["username"],
                                                    conf["db"]["password"], conf["db"]["host"], conf["db"]["name"]))
    base.metadata.create_all(engine)
    return scoped_session(sessionmaker())(bind=engine)


def get_clients(session):
    return session.query(Client).all()
