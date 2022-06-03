import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

base = declarative_base()


class Client(base):
    """Client table in db"""
    __tablename__ = "clients"
    username = Column(String(255), primary_key=True)
    email = Column(String(255), nullable=False)

    websites = relationship("Website")

    @property
    def serialized(self):
        """Serializes client object"""
        return {
            "username": self.username,
            "email": self.email,
            "websites": self.websites
        }


class Website(base):
    """Website table in db"""
    __tablename__ = "websites"
    id = Column(String(255), primary_key=True)
    domain = Column(String(255), nullable=False)
    username = Column(String(255), ForeignKey("clients.username"), nullable=False)

    keywords = relationship("Keyword")

    @property
    def serialized(self):
        """Serializes client object"""
        return {
            "id": self.id,
            "domain": self.domain,
            "keywords": self.keywords
        }


class Keyword(base):
    """Website table in db"""
    __tablename__ = "keywords"
    id = Column(String(255), primary_key=True)
    websiteId = Column(String(255), ForeignKey("websites.id"))
    name = Column(String(255), nullable=False)

    website = relationship("Website", viewonly=True)

    @property
    def serialized(self):
        """Serializes client object"""
        return {
            "id": self.id,
            "name": self.name,
            "latest": self.latest,
            "best": self.best
        }


class Trend(base):
    """Statistics table in db"""
    __tablename__ = "trends"
    id = Column(String(255), primary_key=True)
    keyword = Column(String(255), ForeignKey("keywords.id"))
    position = Column(Integer, nullable=False)
    engine = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)

    @property
    def serialized(self):
        """Serializes client object"""
        return {
            "id": self.id,
            "keyword": self.keyword,
            "position": self.position,
            "engine": self.engine,
            "date":self.date
        }
