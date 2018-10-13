from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import jsonify
from flask import request
import random

# to initialize db, type 'flask db init' in command shell
# next type 'flask db upgrade' and 'flask db migrate'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

db.create_all()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Waypoint(db.Model):
    __tablename__ = 'waypoint'

    id = db.Column(db.Integer, primary_key = True)          
    name = db.Column(db.String(64), index = True)
    latitude = db.Column(db.Float(128), index = True)
    longitude = db.Column(db.Float(128), index = True)
    altitude = db.Column(db.Float(128), index = True)

    def serialize(self):                        # serializes the data 
        return{
            'id': self.id,
            'name': self.name,
            'latitude':self.latitude,
            'longitude':self.longitude,
            'altitude':self.altitude
        }

    def __repr__(self):
        return '<Waypoint %r>' % (self.name)

    
@app.route('/add/', methods = ['POST','GET','DELETE'])   # different outputs whether we are POSTing or GETting
def add():
    if request.method == 'POST':            # gets the body that was created in Postman
        form = request.form
        print(form)
        id = random.randint(1,1000000000)
        print("ID " + id + " was created!")
        name = form['name']                 # sets the name to the name that was posted in Postman
        latitude = form['latitude'] 
        longitude = form['longitude']
        altitude = form['altitude']
        u = Waypoint(id = id, name = name, latitude = latitude, longitude = longitude, altitude = altitude)
        print("user created", u)
        db.session.add(u)
        db.session.commit()
        return jsonify(u.serialize())       # makes it so that the server treats the output as json

    elif request.method == 'DELETE':
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print('Clear table %s' % table)
            session.execute(table.delete())
    session.commit()
    return "Data was reset!"
    else:
        return "oh, fuck, shit, bitch!"

@app.route('/delete/')
def delete():
    u = Waypoint.query.get(i)
    db.session.delete(u)
    db.session.commit()
    return "user deleted"

@app.route('/all/')
def all():
    u = Waypoint.query.all()
    return jsonify([x.serialize() for x in u])      # returns the content in the db in json format in Postman

if __name__ == '__main__':
    app.run(debug=True)
    app.run()