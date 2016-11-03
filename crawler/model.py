import os

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Float
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
    fullname = Column(String, nullable=True)
    location = Column(String, nullable=False)

    def __repr__(self):
        return "User({}({}), '{}')".format(self.username, self.fullname, self.location)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Nothing:
    pass

user = Nothing()

def exists_user(username):
    return session.query(User.username).filter(User.username == username).one_or_none() is not None

def add_user(username, fullname, location):
    if exists_user(username):
        return

    user = User(username=username,
            fullname=fullname,
            location=location)
    session.add(user)
    session.commit()

def get_users():
    return session.query(User).all()

user.exists = exists_user
user.add = add_user
user.get_all = get_users
