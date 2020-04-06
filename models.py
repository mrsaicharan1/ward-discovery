import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

def generate_uuid():
    x = uuid.uuid4()
    return str(x)

class Providers(Base):
    __tablename__ = 'Providers'

    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120), unique=True)
    wards_available = db.Column(db.Integer, default=0)
    wards = db.relationship('Ward', backref='provider')

    def __init__(self, name=None, password=None, email=None, address=None, wards_available=0):
        self.provider_id = generate_uuid()
        self.name = Name
        self.password = password
        self.email = email
        self.address = address
        self.wards_available = wards_available

class Users(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    # hospital_id = 
    hospital_name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120), unique=True)
    
    

    def __init__(self, name=None, password=None, email=None, address=None, hospital=None):
        self.provider_id = generate_uuid()
        self.name = Name
        self.password = password
        self.email = email
        self.address = address
        self.hospital = hospital

class Wards(Base):
    __tablename__ = 'Wards'

    id = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, unique=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.provider_id'))
    status = db.Column(db.Boolean, default=False)

    def __init__(self, ward_id=None, status=0):
        self.ward_id = ward_id
        self.status = status

# Create tables.
Base.metadata.create_all(bind=engine)
