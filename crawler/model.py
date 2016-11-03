import os

from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

home = os.path.expanduser('~')
ghmap_path = '{}/.ghmap'.format(home)

if not os.path.exists(ghmap_path):
    os.makedirs(ghmap_path)

dburl = 'sqlite:///{}/data.db'.format(ghmap_path)

engine = create_engine(dburl)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    location = Column(String)

    def __repr__(self):
        return "<User(username='{}', location='{}')>".format(self.username, self.location)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def exists_user(username):
    return session.query(User).filter(User.username == username).one_or_none() is not None

def add_user(username, location):
    if exists_user(username):
        return

    user = User(username=username, location=location)
    session.add(user)
    session.commit()

