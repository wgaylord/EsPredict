import requests

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

from apscheduler.schedulers.blocking import BlockingScheduler

import time
from xml.etree import ElementTree

PSKReporterURL = "https://retrieve.pskreporter.info/query?noactive=1&rronly=1&flowStartSeconds=900&frange=50000000-51000000&appcontact=chibill110@gmail.com"
RTSWProtonURL =  "https://services.swpc.noaa.gov/json/rtsw/rtsw_wind_1m.json"
RTSWMagneticURL = "https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json"
GOESElectronURL = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-6-hour.json"
GOESProtonURL = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-6-hour.json"
GOESMagenticURL = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-6-hour.json"
GOESXray = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"
 
scheduler = BlockingScheduler() 

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
    ProtonTemperature = Column(Integer)
    InterplanetaryMagneticFieldStrength = Column(Float)
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

def CollectData():
    now = int(time.time())
    pskReportData = ElementTree.fromstring(requests.get(PSKReporterURL).text)
    reports = pskReportData.getchildren()[2:]
    for x in reports:
        ses.add(ReceptionReport(RecordedTime=now,ReportedTime=int(x["flowStartSeconds"]),ReceiverCallsign=x["receiverCallsign"],SenderCallsign=x["senderCallsign"],ReceiverLocator=x["receiverLocator"],SenderLocator=x["senderLocator"],Mode=x["mode"],Frequency=x["frequency"]))
    
    rtswProtonData = requests.get(RTSWProtonURL).json()[:15]
    proton_speed = 0
    proton_density = 0
    proton_temperature = 0
    for x in rtswProtonData:
        proton_speed += x["proton_speed"]
        proton_density += x["proton_density"]
        proton_temperature += x["proton_temperature"]
    proton_speed = proton_speed/15
    proton_density = proton_density/15
    proton_temperature = proton_temperature/15
    
    rtswMagData = requests.get(RTSWMagneticURL).json()[:15]
    bt = 0
    for x in rtswMagData:
        bt += x["bt"]
    bt = bt/15
    
    electronFlux = reuqests.get(GOESElectronURL).json()[-1]["flux"]
    
    protonFluxData = requests.get(GOESProtonURL).json()[-32:]
    mev1 = (protonFluxData[0]["flux"] + protonFluxData[8]["flux"] + protonFluxData[16]["flux"] + protonFluxData[24]["flux"])/4
    mev10 = (protonFluxData[1]["flux"] + protonFluxData[9]["flux"] + protonFluxData[17]["flux"] + protonFluxData[25]["flux"])/4
    mev100 = (protonFluxData[2]["flux"] + protonFluxData[10]["flux"] + protonFluxData[18]["flux"] + protonFluxData[26]["flux"])/4
    mev30 = (protonFluxData[3]["flux"] + protonFluxData[11]["flux"] + protonFluxData[19]["flux"] + protonFluxData[27]["flux"])/4
    mev5 = (protonFluxData[4]["flux"] + protonFluxData[12]["flux"] + protonFluxData[20]["flux"] + protonFluxData[28]["flux"])/4
    mev50 = (protonFluxData[5]["flux"] + protonFluxData[13]["flux"] + protonFluxData[21]["flux"] + protonFluxData[29]["flux"])/4
    mev500 = (protonFluxData[6]["flux"] + protonFluxData[14]["flux"] + protonFluxData[22]["flux"] + protonFluxData[30]["flux"])/4
    mev60 =  (protonFluxData[7]["flux"] + protonFluxData[15]["flux"] + protonFluxData[23]["flux"] + protonFluxData[31]["flux"])/4
  
    GoesMagData = requests.get(GOESMagenticURL).json()[-4:]
    Hp = 0
    for x in GoesMagData:
        Hp += Hp["Hp"]
    Hp = Hp/4
    
    GoesXray = requests.get(GOESXray).json()[-4:]
    xray4 = (GoesXray[0] + GoesXray[2])/2
    xray8 = (GoesXray[1] + GoesXray[3])/2
    
    ses.add(SpaceWeatherReport(RecordedTime=now,ProtonSpeed=proton_speed,ProtonDensity=proton_density,ProtonTemperature=proton_temperature,InterplanetaryMagneticFieldStrength=bt,IntegralElectrons=electronFlux,IntegralProtons1MeV=mev1,IntegralProtons5MeV=mev5,IntegralProtons10MeV=mev10,IntegralProtons30MeV=mev30,IntegralProtons50MeV=mev50,IntegralProtons60MeV=mev60,IntegralProtons100MeV=mev100,IntegralProtons500MeV=mev500,MagneticFieldStrength=Hp,Xrays8=xray8,Xrays4=xrays4))
    ses.commit()
    
scheduler.add_job(CollectData,'interval',minutes=15)


try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
