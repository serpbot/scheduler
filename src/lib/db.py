#!/usr/bin/env python3
"""
This module empasses various functions used to query the database
"""
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.model.orm import base, Client

log = logging.getLogger(__name__)


def get_db_session():
    """Get db session"""
    engine = create_engine("mysql://%s:%s@%s/%s" % (os.environ.get("DATABASE_USERNAME"),
                                                    os.environ.get("DATABASE_PASSWORD"),
                                                    os.environ.get("DATABASE_HOST"),
                                                    os.environ.get("DATABASE_NAME")))
    base.metadata.create_all(engine)
    return scoped_session(sessionmaker())(bind=engine)


def get_clients(session):
    return session.query(Client).all()
