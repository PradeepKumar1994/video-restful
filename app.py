# -*- coding: utf-8 -*-
"""
Created on Mon May 25 23:30:40 2020

@author: prade
"""

import flask
from flask import Flask, request, Response
from database.db import initialize_database
from database.models import Data_create

from werkzeug.utils import secure_filename


application = flask.Flask(__name__)


#data = [{
#        "name": "The Shawshank Redemption",
#        "casts": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"],
#        "genres": ["Drama"]
#    },
#    {
#       "name": "The Godfather ",
#       "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
#       "genres": ["Crime", "Drama"]
#    }
#]


application.config['MONGO_SETTINGS'] = {'host': 'mongodb://localhost/flask-movie-bag'}
initialize_database(application)


@application.route('/')
def hello():
    
    return {'hello': 'world'}



@application.route('/data')
def get_data():
    
    data = Data_create.objects.to_json()
    
    return Response(data, mimetype="application/json", status=200)




@application.route('/data-add', methods = ['POST'])
def add_movie():
    body = request.get_json()
    data = Data_create(body).save()
    id = data.id
    return {'id': str(id)}, 200

@application.route('/data/<index>', methods=['PUT'])
def update_movie(index):
    body = request.get_json()
    Data_create.objects.get(id=id).update(**body)
    return '', 200

@application.route('/data/<int:index>', methods=['DELETE'])
def delete_movie(index):
    Data.objects.get(id=id).delete()
    return '', 200


@application.route('/upload')
def upload_file():
   return flask.render_template('upload.html')
	
@application.route('/uploader', methods = ['GET', 'POST'])
def upload_file_():
   if flask.request.method == 'POST':
      f = flask.request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


@application.route('/movies/<id>')
def get_movie(id):
    movies = Data_create.objects.get(id=id).to_json()
    return Response(movies, mimetype="application/json", status=200)


application.run()
























