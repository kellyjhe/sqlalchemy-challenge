# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)
session = Session()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return (
    f"Available Routes:<br>"
    f"<a href='/api/v1.0/precipitation'>Precipitation</a><br>"
    f"<a href='/api/v1.0/stations'>Stations</a><br>"
    f"<a href='/api/v1.0/tobs'>Time Observations</a><br>"
    f"<a href='/api/v1.0/<start>'>Start</a><br>"
    f"<a href='/api/v1.0/<start>/<end>'>End</a><br>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the precipitation data from one year ago
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date_int = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date_int - timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago)

    prep_dict = {date: prcp for date, prcp in results}

    return jsonify(prep_dict)
    
@app.route('/api/v1.0/stations')
def get_stations():
    # Return a JSON list of stations from the dataset
    stations = session.query(Station).all()

    station_list = [station.station for station in stations]

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def get_tobs():
    # Query the dates and temp observations of the most active station for the previous year of data
    most_active_station = session.query(Measurement.station, func.count(Measurement.station))\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .first()
    
    print(most_active_station)
    
    # Get the last year of observations
    last_year = datetime.now() - timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station.station)\
        .filter(Measurement.date >= last_year)\
        .all()

    # Create dictionaries
    tobs_list = [{'date': date, 'tobs': tobs} for date, tobs in results]
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def get_temp_stats(start, end=None):
    if end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= end)\
            .all()
    
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .all()
        
    # Create dictionary
    temp_stats = {
        "Temp min": results[0][0],
        "Temp average": results[0][1],
        "Temp max": results[0][2]
    }
    return jsonify(temp_stats)
    
if __name__ == '__main__':
    app.run(debug=True)