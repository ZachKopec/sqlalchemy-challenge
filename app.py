import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect an existing database into a new model
Base = automap_base()
#Reflect the tables
Base.prepare(engine, reflect=True)

#Save reference to the table
measure = Base.classes.measurement
station = Base.classes.station

#Flask Setup
app = Flask(__name__)


#Flask Routes
#Home
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start_end"
     )

#Precipitation
@app.route("/api/v1.0/precipitaion")
def precip():
    #Create session
    session = Session(engine)

    #Perform a query to retrieve the data and precipitation scores
    sel = [measure.date,
           func.avg(measure.prcp)]

    data_agg = session.query(*sel).\
        filter(measure.date > '2016-08-23').\
        group_by(measure.date).\
        order_by(measure.date).all()

    session.close()

    #Convert into normal list
    temp = []
    for date, prcp in data_agg:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        temp.append(precip_dict)

    #JSONIFY
    return jsonify(temp)

#Stations
@app.route("/api/v1.0/stations")
def statsons():
    #Create session
    session = Session(engine)

    #Query all unique stations
    stations = session.query(station.station).\
            order_by(station.station).all()

    session.close()

    #Convert into normal list
    all_stations = []
    for stat in stations:
        station_dict = {}
        station_dict["station"] = stat
        all_stations.append(station_dict)

    JSONIFY
    return jsonify(all_stations)

#tobs
@app.route("/api/v1.0/tobs")
def toobs():
    
    #Create session
    session = Session(engine)

    sel3 = [measure.station,
            measure.date,
            measure.tobs]

    #Query temp info in past year for station
    act_agg = session.query(*sel3).\
        filter(measure.date > '2016-08-23', measure.station == 'USC00519281').\
        group_by(measure.date).\
        order_by(measure.date).all()

    session.close()

    #Convert into normal list
    temp2 = []
    for station, date, tobs in act_agg:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        temp2.append(tobs_dict)

    JSONIFY
    return jsonify(temp2)

#Start
@app.route("/api/v1.0/start")
def start():
    
    #User input
    user_start = input("Please enter a start date in the format: 'YYYY-MM-DD' (Earliest date is 2010-01-01 & latest date is 2017-08-23) ")
    
    #Create session
    session = Session(engine)

    """Return a list of all passenger names"""

    #Query temp info in past year for station
    sel4 = [measure.date,
            func.min(measure.tobs),
            func.max(measure.tobs),
            func.avg(measure.tobs)]

    start_agg = session.query(*sel4).\
        filter(measure.date >= user_start).\
        group_by(measure.date).\
        order_by(measure.date).all()

    session.close()

    #Convert into normal list
    temp4 = []
    for date, min_tobs, max_tobs, avg_tobs in start_agg:
        start_dict = {}
        start_dict["date"] = date
        start_dict["min temp"] = min_tobs
        start_dict["max temp"] = max_tobs
        start_dict["avg. temp"] = avg_tobs

        temp4.append(start_dict)

    JSONIFY
    return jsonify(temp4)

#Start & End
@app.route("/api/v1.0/start_end")
def start_end():
    
    #User input
    user_start = input("Please enter a start date in the format: 'YYYY-MM-DD' (Earliest date is 2010-01-01 & latest date is 2017-08-23) ")
    user_end = input("Please enter an end date in the format: 'YYYY-MM-DD' (Earliest date is 2010-01-01 & latest date is 2017-08-23) ")
    
    #Create Session
    session = Session(engine)

    #Query temp info in past year for station
    sel5 = [measure.date,
            func.min(measure.tobs),
            func.max(measure.tobs),
            func.avg(measure.tobs)]

    start_end_agg = session.query(*sel5).\
        filter(measure.date >= user_start, measure.date <= user_end).\
        group_by(measure.date).\
        order_by(measure.date).all()

    session.close()

    #Conver to normal list
    temp5 = []
    for date, min_tobs, max_tobs, avg_tobs in start_end_agg:
        start_end_dict = {}
        start_end_dict["date"] = date
        start_end_dict["min temp"] = min_tobs
        start_end_dict["max temp"] = max_tobs
        start_end_dict["avg. temp"] = avg_tobs

        temp5.append(start_end_dict)

    #JSONIFY
    return jsonify(temp5)


if __name__ == '__main__':
    app.run(debug=True)
