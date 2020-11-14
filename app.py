import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measure = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start"
#         # f"/api/v1.0/<start>/<end>"
     )


@app.route("/api/v1.0/precipitaion")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    sel = [measure.date,
           func.avg(measure.prcp)]

    data_agg = session.query(*sel).\
        filter(measure.date > '2016-08-23').\
        group_by(measure.date).\
        order_by(measure.date).all()

    session.close()

    # Convert list of tuples into normal list
    temp = []
    for date, prcp in data_agg:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        temp.append(precip_dict)

    return jsonify(temp)


@app.route("/api/v1.0/stations")
def statsons():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all unique stations
    stations = session.query(station.station).\
            order_by(station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for stat in stations:
        station_dict = {}
        station_dict["station"] = stat
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def toobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    sel3 = [measure.station,
            measure.date,
            measure.tobs]

    act_agg = session.query(*sel3).\
        filter(measure.date > '2016-08-23', measure.station == 'USC00519281').\
        group_by(measure.date).\
        order_by(measure.date).all()

    session.close()

    # Convert list of tuples into normal list
    temp2 = []
    for station, date, tobs in act_agg:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        temp2.append(tobs_dict)

    return jsonify(temp2)

@app.route("/api/v1.0/start")
def start():
    
    user_start = input("Please enter a date in the format: 'YYYY-MM-DD' (Earliest date is 2010-01-01 & latest date is 2017-08-23) ")
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""

    # Query all passengers
    sel4 = [measure.date,
            func.min(measure.tobs),
            func.max(measure.tobs),
            func.avg(measure.tobs)]

    start_agg = session.query(*sel4).\
        filter(measure.date >= user_start).\
        group_by(measure.date).\
        order_by(measure.date).all()

    session.close()

    # Convert list of tuples into normal list
    temp4 = []
    for date, min_tobs, max_tobs, avg_tobs in start_agg:
        start_dict = {}
        start_dict["date"] = date
        start_dict["min temp"] = min_tobs
        start_dict["max temp"] = max_tobs
        start_dict["avg. temp"] = avg_tobs

        temp4.append(start_dict)

    return jsonify(temp4)

# @app.route("/api/v1.0/<start>/<end>")
# def names():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(temp.name).all()

#     session.close()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)


if __name__ == '__main__':
    app.run(debug=True)
