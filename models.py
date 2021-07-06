from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(100))
    place_address = db.Column(db.String(100))
    operation = db.relationship("Operation", back_populates="place",  uselist=False)

    def __init__(self, place_name, place_address):
        self.place_name = place_name
        self.place_address = place_address

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'place_name': self.place_name,
            'place_address': self.place_address,
        }

class Operation(db.Model):
    __tablename__ = 'operation'

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, ForeignKey('place.id'))
    place = db.relationship("Place", back_populates="operation")
    start_time= db.Column(db.Date)
    end_time = db.Column(db.Date)
    round_count = db.Column(db.Integer())
    signals = db.relationship("Signals",backref='operation', lazy=True)


    def __init__(self, place_id, start_time, end_time,round_count):
        self.place_id = place_id
        self.start_time = start_time
        self.end_time = end_time
        self.round_count = round_count

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'place_id':self.place_id,
            'place_name': self.start_time,
            'end_time': self.end_time,
            'round_count' : self.round_count,

        }


class Signals(db.Model):
    __tablename__ = 'signals'
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.Integer(), ForeignKey('operation.id'))
    bssid= db.Column(db.String(100))
    ssid = db.Column(db.String(100))
    frequency = db.Column(db.Integer)
    signal_level = db.Column(db.Integer)
    sample_count = db.Column(db.Integer)

    def __init__(self, operation_id, bssid, ssid, frequency, signal_level, sample_count):
        self.operation_id = operation_id
        self.bssid = bssid
        self.ssid = ssid
        self.frequency = frequency
        self.signal_level = signal_level
        self.sample_count = sample_count

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'operation_id' : self.operation_id,
            'bssid': self.bssid,
            'ssid': self.ssid,
            'frequency' : self.frequency,
            'signal_level' : self.signal_level,
            'sample_count' : self.sample_count
        }