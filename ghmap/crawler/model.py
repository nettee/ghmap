import os

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Float, ForeignKey
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

    headers = ('username', 'fullname', 'location')

    username = Column(String, primary_key=True)
    fullname = Column(String, nullable=True)
    location = Column(String, nullable=False)

    def asdict(self):
        return {attr: getattr(self, attr) for attr in self.headers} 

    def __repr__(self):
        return "User[{}({}), '{}']".format(self.username, self.fullname, self.location)

class Geocode(Base):

    __tablename__ = 'geocodes'

    headers = ('location', 'address', 'latitude', 'longitude')

    location = Column(String, ForeignKey('users.location'), primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def asdict(self):
        return {attr: getattr(self, attr) for attr in self.headers}

    def __repr__(self):
        return "{}: ({}, {}), {}".format(self.location, self.latitude, self.longitude, self.address)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Nothing:
    pass

user = Nothing()
geocode = Nothing()

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
    users = session.query(User).all() 
    return [user.asdict() for user in users]

def exists_geocode(location):
    return session.query(Geocode.location).filter(Geocode.location == location).one_or_none() is not None

def add_geocode(location, address, latitude, longitude):
    if exists_geocode(location):
        return

    geocode = Geocode(location=location,
            address=address,
            latitude=latitude,
            longitude=longitude)
    session.add(geocode)
    session.commit()

def get_geocodes(location):
    users = session.query(Geocode).filter(Geocode.location == location).all()
    return [user.asdict() for user in users]

user.exists = exists_user
user.add = add_user
user.get_all = get_users
geocode.exists = exists_geocode
geocode.add = add_geocode
geocode.get_all = get_geocodes

def get_users_geocodes():
    users_geocodes = session.query(User, Geocode).filter(User.location == Geocode.location).all()
    result = []
    for (user, geocode) in users_geocodes:
        userdict = user.asdict()
        geocodedict = geocode.asdict()
        del userdict['location']
        del geocodedict['location']
        userdict.update(geocodedict)
        result.append(userdict)
    return result


