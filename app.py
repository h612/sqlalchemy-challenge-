# 1. Import Flask
from flask import Flask


# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def index():
    msg="""
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/<start> and /api/v1.0/<start>/<end>"""
    return msg


@app.route("/api/v1.0/precipitation")
def precip():
    p='''Convert the query results to a dictionary using date as the key and prcp as the value.


    Return the JSON representation of your dictionary.'''

    return p


@app.route("/api/v1.0/stations")
def stations():
    st = """Return a JSON list of stations from the dataset."""

    return f"{st}."

@app.route("/api/v1.0/tobs")
def tobs():
    t = """Query the dates and temperature observations of the most active station for the last year of data.


            Return a JSON list of temperature observations (TOBS) for the previous year."""

    return f"{t}."

# @app.route("/api/v1.0/<start> and /api/v1.0/<start>/<end>")
# def tempDate():
#     td = """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


#     When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


#     When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""

#     return f"{td}."

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
