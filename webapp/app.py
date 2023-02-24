import flask
import pandas as pd
import pickle

from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.orm import backref

# from models import db, CountiesModel, PlacesModel

# Use pickle to load in the pre-trained model.
with open(f'model/weather_model_two.pkl', 'rb') as f:
    model = pickle.load(f)
app = flask.Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Bowen123@localhost:5432/tourism_ke"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
CORS(app)

class CountiesModel(db.Model):
    __tablename__ = 'counties_table'

    id = db.Column(db.Integer, primary_key=True)
    county_name = db.Column(db.String())
    change_rate = db.Column(db.Float())

    def __init__(self, county_name, change_rate):
        self.county_name = county_name
        self.change_rate = change_rate

    def __repr__(self):
        return f"{self.county_name}:{self.change_rate}"

class PlacesModel(db.Model):
    __tablename__ = 'places_table'

    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String())
    place_description = db.Column(db.String())
    place_picture = db.Column(db.String())
    place_map = db.Column(db.String())
    county_id = db.Column(db.Integer, db.ForeignKey('counties_table.id'))
    county = db.relationship("CountiesModel", backref=backref("request", uselist=False))



@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        print("We are here")
        return (flask.render_template('main.html'))
    if flask.request.method == 'POST':
        temperature = flask.request.form['temperature']
        rainfall = flask.request.form['humidity']
        month = flask.request.form['month-today']
        place = flask.request.form['select_place']
        print(place.title())
        data = CountiesModel.query.filter_by(county_name='Narok').first()
        print(data)
        months = [0] * 11

        if month == 1:
            months[3] = 1
        elif month == 2:
            months[6] = 1
        elif month == 3:
            months[0] = 1
        elif month == 4:
            months[7] = 1
        elif month == 5:
            months[5] = 1
        elif month == 6:
            months[4] = 1
        elif month == 7:
            months[1] = 1
        elif month == 8:
            months[10] = 1
        elif month == 9:
            months[9] = 1
        elif month == 10:
            months[8] = 1
        elif month == 11:
            months[2] = 1
        else:
            months = months

        input_variables = pd.DataFrame([[rainfall, temperature, *months]],
                                       columns=[
                                           'Rainfall - (MM)',
                                           'Temperature - (Celsius)',
                                           'Apr Average',
                                           'Aug Average',
                                           'Dec Average',
                                           'Feb Average',
                                           'Jul Average',
                                           'Jun Average',
                                           'Mar Average',
                                           'May Average',
                                           'Nov Average',
                                           'Oct Average',
                                           'Sep Average',
                                       ],
                                       dtype=float)
        prediction = model.predict(input_variables)[0]
        return flask.render_template('main.html',
                                     original_input={'Temperature': temperature,
                                                     'Rainfall': rainfall},
                                     result=prediction,
                                     )


if __name__ == '__main__':
    app.run(debug=True)

