# Import the dependencies.
from flask import Flask, jsonify

import pandas as pd
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return(
        f'Available Routes: <br/>'
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/temp/<start>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    recent = dt.date(2017, 8, 23)
    previous_yr = recent - dt.timedelta(365)
    p = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_yr).all()
    p_dict = {
        date: prcp for date, prcp in p
    }
    return jsonify(p_dict)

@app.route('/api/v1.0/stations')
def stations():
    s = session.query(Station.station).all()
    s_list = list(np.ravel(s))
    return jsonify(s_list)

@app.route('/api/v1.0/tobs')
def tobs():
    most_active_id = 'USC00519281'
    recent = dt.date(2017, 8, 23)
    previous_yr = recent - dt.timedelta(365)
    t = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= previous_yr).\
    filter(Measurement.station == most_active_id).all()
    t_list = list(np.ravel(t))
    return jsonify(t_list)

@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/<start>/<end>')
def start_end(start = None, end = None):
    if not end:
        q = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        q_list = list(np.ravel(q))
        return jsonify(q_list)
    q_we = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    q_we_list = list(np.ravel(q_we))
    return jsonify(q_we_list)
