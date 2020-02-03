import requests

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///data.db')

Base = declarative_base()
 
class ReceptionReport(Base):
    __tablename__ = "ReceptionReports"
 
    Id = Column(Integer, primary_key=True)
    RecordedTime = Column(Integer) #Time recorded into the DB
    ReportedTime = Column(Integer) #Time according to PSKReporter it was recieved
    ReceiverCallsign = Column(String)
    SenderCallsign = Column(String)
    ReceiverLocator = Column(String)  
    SenderLocator = Column(String) 
    Mode = Column(String)
    Frequency = Column(Integer) #In Hz
    
class SpaceWeatherReport(Base):
    __tablename__ = "SpaceWeatherReports"
    
    Id = Column(Integer, primary_key=True)
    RecordedTime = Column(Integer) #Time recorded into the DB
    ProtonSpeed = Column(Float)
    ProtonDensity = Column(Float)
    IntegralElectrons = Column(Float)
    IntegralProtons1MeV = Column(Float)
    IntegralProtons5MeV = Column(Float)
    IntegralProtons10MeV = Column(Float)
    IntegralProtons30MeV = Column(Float)
    IntegralProtons50MeV = Column(Float)
    IntegralProtons60MeV = Column(Float)
    IntegralProtons100MeV = Column(Float)
    IntegralProtons500MeV = Column(Float)
    MagneticFieldStrength = Column(Float)
    Xrays8 = Column(Float)
    Xrays4 = Column(Float)
   
 
    
    
Session = sessionmaker(bind=eng)
ses = Session()    
