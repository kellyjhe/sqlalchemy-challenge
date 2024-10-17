# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, automap_base
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
    return '''
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/<start><br>
    /api/v1.0/<start>/<end><br>
    '''
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
def stations():


@app.route('/api/v1.0/tobs')
def tobs():
    

    
