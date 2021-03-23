import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#save dates in variable
most_recent_datetime = dt.date(2017, 8, 23)
one_year_date = most_recent_datetime - dt.timedelta(days = 365)

# Create an app, being sure to pass __name__
app = Flask(__name__)


# Flask Routes
@app.route("/")
def home():
    return (
        f"Welcome to 'Home' page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_date).all()

    session.close()

    # Create a dictionary from the row data 
    prcp_dict = {}
    for date, prcp in results:
        prcp_dict.setdefault(date, prcp)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query date and temperature for the last year of data

    first_id = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()
    station_id = first_id[0]

    temperature_results = session.query(Measurement.tobs, Measurement.station).filter(Measurement.date >= one_year_date).filter(Measurement.station == station_id).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    temperature_data = []
    for tobs, station in temperature_results:
        temperature_dict = {}
        temperature_dict["tobs"] = tobs
        temperature_dict["station"] = station
        temperature_data.append(temperature_dict)

    return jsonify(temperature_data)





if __name__ == "__main__":
    app.run(debug=True)