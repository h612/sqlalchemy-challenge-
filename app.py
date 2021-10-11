# 1. Import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# 1. Data Base setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
measurement=Base.classes.measurement
station=Base.classes.station
# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def index():
     """List all available api routes."""
     return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        
    )


@app.route("/api/v1.0/precipitation")
def precip():
    # Calculate the date 1 year ago from the last data point in the database
    session=Session(engine)
    lastDate=session.query(measurement.date).order_by(measurement.date.desc()).first()
    lastDate=list(lastDate)
    dt_last_Date=dt.datetime.strptime(lastDate[0],"%Y-%m-%d").date()
    query_date=dt_last_Date-dt.timedelta(days=365)
    prcpLastYear=session.query(measurement.date,measurement.prcp).\
         filter(measurement.date>=query_date).order_by(measurement.date).all()
    session.close()
    p='''Convert the query results to a dictionary using date as the key and prcp as the value.
   Return the JSON representation of your dictionary.'''
    all_prec=[]
    for date,prcp in prcpLastYear:
        prec={}
        prec["date"]=date
        prec["prcp"]=prcp
        all_prec.append(prec)
    
    return jsonify(all_prec)


@app.route("/api/v1.0/stations")
def stations():
     
     session=Session(engine)
     st=session.query(measurement.station).distinct()
     session.close()
     sts = "Return a JSON list of stations from the dataset."
     stl=[]
     for s in st:
          stl.append(s)
     return jsonify(stl)

@app.route("/api/v1.0/tobs")
def tobs():
     
     session=Session(engine)
     t = """Query the dates and temperature observations of the most active station for the last year of data.
          Return a JSON list of temperature observations (TOBS) for the previous year."""
     lastDate=session.query(measurement.date).order_by(measurement.date.desc()).first()
     lastDate=list(lastDate)
     dt_last_Date=dt.datetime.strptime(lastDate[0],"%Y-%m-%d").date()
     query_date=dt_last_Date-dt.timedelta(days=365)
     active_st=session.query(measurement.station,func.count(measurement.station)).\
          group_by(measurement.station).\
          order_by(func.count(measurement.station).desc()).first()
     tobsYear=session.query(measurement.tobs).\
          filter(measurement.date>=query_date).\
          filter(measurement.station==active_st[0]).all()
     session.close()
     tl=[]
     for t in tobsYear:
          tl.append(t)
     return jsonify(tl)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def tempDateSE(start=None,end=None):
     session=Session(engine)

     temperature_data = session.query(func.min(measurement.tobs),\
                                func.avg(measurement.tobs),\
                                func.max(measurement.tobs)).\
                                filter(measurement.date >= start).\
                                filter(measurement.date<=end).all()

     session.close()

     temp_all = []
     for min, avg, max in temperature_data:
        temp_dict = {}
        temp_dict["Min"] = min
        temp_dict["Average"] = avg
        temp_dict["Max"] = max
        temp_all.append(temp_dict)

     return jsonify(temp_all)
# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
