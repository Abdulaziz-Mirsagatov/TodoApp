from tabnanny import check
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.db'

class Cities(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    temp = db.Column(db.Float())
    description = db.Column(db.String(50))

# city = 'London'
# r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=738133d618da2a2fc537b15f37e93b6a")
# data = r.json()
# print(data)


@app.route('/')
def home():
    data_list = Cities.query.all()
    for city in data_list:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid=738133d618da2a2fc537b15f37e93b6a")
        data = r.json()
        city.name = data['name']
        city.temp = data['main']['temp']
        city.description = data['weather'][0]['description']
    return render_template('home.html', data_list=data_list)

@app.route('/add-city', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        city = request.form['city']
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=738133d618da2a2fc537b15f37e93b6a")
        data = r.json()
        city = Cities(name=data['name'], temp=data['main']['temp'], description=data['weather'][0]['description'])
        db.session.add(city)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add-city.html')

@app.route('/remove-city', methods=['GET', 'POST'])
def remove_city():
    if request.method == 'POST':
        cities = Cities.query.all()
        for city in cities:
            if city.name in request.form:
                checkbox = request.form[city.name]
                db.session.delete(city)
                db.session.commit()
        return redirect('/')
    else:
        data_list = Cities.query.all()
        for city in data_list:
            r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid=738133d618da2a2fc537b15f37e93b6a")
            data = r.json()
            city.name = data['name']
            city.temp = data['main']['temp']
            city.description = data['weather'][0]['description']
        return render_template('remove-city.html', data_list=data_list)

if __name__ == 'main':
    app.run(debug=True)