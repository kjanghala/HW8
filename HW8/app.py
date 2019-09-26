import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and respective precipitation levels in the last year of data"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').all()
    
    date_list = []
    prcp_list = []
    for date, prcp in results:
        date_list.append(date)
        prcp_list.append(prcp)

    date_prcp = dict(zip(date_list, prcp_list))
    print(date_prcp)
    
    return jsonify(date_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    session = Session(engine)
    results = session.query(Station.name).all()

    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all observations"""
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.date > '2016-08-22').all()
       
    yr_tobs = list(np.ravel(results))
        
    return jsonify(yr_tobs)

if __name__ == '__main__':
    app.run(debug=True)
