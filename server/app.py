#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api =Api(app)
# don't forget this! to init RESTful 


@app.route('/')
def home():
    return ''

class Scientists(Resource):

    def get(self):
        scientists = [scientist.to_dict(rules=('-missions', '-planets',))
                      for scientist in Scientist.query.all()]

        return make_response(scientists, 200)

    def post(self):

        fields = request.get_json()
        try:
            scientist = Scientist(
                name=fields['name'],
                field_of_study=fields['field_of_study']
            )
            db.session.add(scientist)
            db.session.commit()
            return make_response(scientist.to_dict(rules=('-missions',)), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)

api.add_resource(Scientists, "/scientists")

class SceinetistId(Resource):
    pass 

class Planets(Resource):
    pass 

class Missions(Resource):
    pass 


if __name__ == '__main__':
    app.run(port=5555, debug=True)
