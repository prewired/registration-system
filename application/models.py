from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime,\
    Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

connection_string = "sqlite:///registration.db.sqlite"
engine = create_engine(connection_string)
Sess = sessionmaker(bind=engine)
session = scoped_session(Sess)

Base = declarative_base()
Base.query = session.query_property()

def create_all():
    Base.metadata.create_all(engine)

class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    allergies_diatary = Column(Text)
    medication = Column(Text)
    illnesses_injuries_conditions = Column(Text)
    projects = Column(Text)
    emergency_contact_name = Column(String)
    emergency_contact_relationship = Column(String)
    emergency_contact_phone = Column(String)
    emergency_contact_email = Column(String)
    photo_consent = Column(Boolean)
    form_filled_by = Column(String)
    month_year_of_birth = Column(Date)
    is_member = Column(Boolean)
    registered_for_id = Column(ForeignKey("sessions.id"))

    attendances = relationship("Attendance",
        cascade="all, delete, delete-orphan", backref="attendee")

    def __repr__(self):
        return "<Attendee: {}>".format(self.name)

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    attendances = relationship("Attendance",
        cascade="all, delete, delete-orphan", backref="visitor")

    def __repr__(self):
        return "<Visitor: {}>".format(self.name)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)

    registrations = relationship("Attendee",
        cascade="all, delete, delete-orphan", backref="registered_for")

    attendances = relationship("Attendance",
            cascade="all, delete, delete-orphan", backref="session")

    def __repr__(self):
        return "<Session: {}>".format(self.start)

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True)
    attendee_id = Column(ForeignKey("attendees.id"))
    visitor_id = Column(ForeignKey("visitors.id"))
    session_id = Column(ForeignKey("sessions.id"))
    time_in = Column(DateTime)
    time_out = Column(DateTime)

    def __repr__(self):
        return "<Attendance: {}>".format(self.id)
