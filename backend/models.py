from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)

class SubTopic(Base):
    __tablename__ = 'LMSSubTopicMaster'

    SubTopicID = Column(Integer, primary_key=True, index=True)
    SubTopic = Column(String)
    
    # Optional relationship backref
    videos = relationship('VideoContent', back_populates='subtopic')

class VideoContent(Base):
    __tablename__ = 'LMSVideoContents'

    VCId = Column(Integer, primary_key=True, index=True)
    SubTopicID = Column(Integer, ForeignKey('LMSSubTopicMaster.SubTopicID'))
    VideoCaption = Column(String)
    VideoFileName = Column(String)
    Thumbnail = Column(String)

    subtopic = relationship('SubTopic', back_populates='videos')
