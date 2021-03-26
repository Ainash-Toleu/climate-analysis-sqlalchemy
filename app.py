import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Save dates in variable
recent_date = dt.date(2017, 8, 23)
last_year = recent_date - dt.timedelta(days = 365)

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    return (
        f"Welcome to 'Home' page!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation route:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"(Returns precipitation data for the last year in the database)<br/>"
        f"<br/>"
        f"Stations route:<br/>"
        f"/api/v1.0/stations<br/>"
        f"(Returns list of all the stations in the database)<br/>"
        f"<br/>"
        f"Tobs route:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"(Returns data for the most active station for the last year in the database)<br/>"
        f"<br/>"
        f"Start date route:<br/>"
        f"/api/v1.0/<start><br/>"
        f"(Returns the min,max,avg temperature from the given start date(0000-00-00) in the database)<br/>"
        "<br/>"
        f"Start/End dates route:<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"(Returns the min,max,avg temperature from the given start date(0000-00-00) to the given end date(0000-00-00) in the database)<br/>"
    )
        
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    # Create a dictionary from the row data 
    prcp_dict = {}
    for date, prcp in results:
        prcp_dict.setdefault(date, prcp)
    
    # Return JSON
    return jsonify(prcp_dict)

    #Close session
    session.close()

@app.route("/api/v1.0/stations")
def stations():

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    # Returns JSON
    return jsonify(all_stations)

    #Close session
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query date and temperature for the last year of data
    first_id = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()
    station_id = first_id[0]
    temperature_results = session.query(Measurement.tobs, Measurement.station).filter(Measurement.date >= last_year).filter(Measurement.station == station_id).all()

    # Create a dictionary from the row data and append to a list 
    temperature_data = []
    for tobs, station in temperature_results:
        temperature_dict = {}
        temperature_dict["tobs"] = tobs
        temperature_dict["station"] = station
        temperature_data.append(temperature_dict)

    # Return JSON
    return jsonify(temperature_data)

    #Close session
    session.close()

@app.route("/api/v1.0/<start>")
def start(start=None):
    
    # Create session (link) from Python to the DB
    session = Session(engine)

    #Convert the date from string
    start_date = dt.datetime.strptime(start,"%Y-%m-%d")

    #Calculate the min,max and avg temperature
    summary_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    # Convert list of tuples into normal list
    start_data = list(np.ravel(summary_data))

    # Return JSON
    return jsonify(start_data)

    #Close session
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):

    # Create session (link) from Python to the DB
    session = Session(engine)
    
    #Convert dates from string
    start_date = dt.datetime.strptime(start,"%Y-%m-%d")
    end_date = dt.datetime.strptime(end,"%Y-%m-%d")

    #Calculate the min,max and avg temperature
    summary_all = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
   
    # Convert list of tuples into normal list
    start_end_data = list(np.ravel(summary_all))
    
    # Return JSON
    return jsonify(start_end_data)

    #Close session
    session.close()



if __name__ == "__main__":
    app.run(debug=True)