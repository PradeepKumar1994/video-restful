# -*- coding: utf-8 -*-
"""
Created on Mon May 25 23:30:40 2020

@author: prade
"""

import flask
from flask import Flask, request, Response, redirect
#from database.db import initialize_database
#from database.models import Data_create
#import pymongo
from werkzeug.utils import secure_filename
import datetime
import requests
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

#
#application.config['MONGO_SETTINGS'] = {'host': 'mongodb://localhost/flask-movie-bag'}
#initialize_database(application)
#client = pymongo.MongoClient("mongodb://admin:admin@mongodb-atlas-shard-00-00-afdbx.mongodb.net:27017,mongodb-atlas-shard-00-01-afdbx.mongodb.net:27017,mongodb-atlas-shard-00-02-afdbx.mongodb.net:27017/test?ssl=true&replicaSet=MongoDB-Atlas-shard-0&authSource=admin&retryWrites=true&w=majority")

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
    Data_create.objects.get(id=id).delete()
    return '', 200


@application.route('/upload')
def upload_file():
   return flask.render_template('upload.html')

def rename_file(filename):
    
    temp = filename.rsplit('.', 1)
        
    filename_ = str(datetime.datetime.now())[:-7] + "." + temp[1]
    
    return filename_
         
        	          

@application.route('/uploader', methods = ['GET', 'POST'])
def upload_file_():
        

    if flask.request.method == 'POST':
        
        f = flask.request.files['file']
      
        filename_ = rename_file(f.filename)
        
        """  hdfs_directory_folder_check - contains the date in yyyy-mm-dd """
        hdfs_directory_folder_check, hdfs_filename = (filename_).split(' ')[0], (filename_).split(' ')[1]
        
        print("hdfs_directory_folder_check", hdfs_directory_folder_check)
      
      
        """  hdfs_directory_api_check - contains the api to 
        directory(hdfs_directory_folder_check) name """
        hdfs_directory_api_check = "http://skywalker-G7-7588:50070/webhdfs/v1/test/"+hdfs_directory_folder_check+"/?op=GETFILESTATUS"
      
        hdfs_directory_status = str(requests.get(hdfs_directory_api_check)).split(' ')[1][1:4]

        print("Status is : {}".format(hdfs_directory_status))
        
        if(hdfs_directory_status == "200"):
            
            f.save(secure_filename(filename_.split(" ")[1]))
          
            print("--- Directory exists. Sending the file ---")
            
            #headers = {'Content-type': 'application/octet-stream'}
            
            response = requests.get("http://skywalker-G7-7588:50070/webhdfs/v1/test/"+hdfs_directory_folder_check+"/"+hdfs_filename+"?op=CREATE", allow_redirects = True)
            
            print(response.status_code)
            
            print(response.url)
            
            print(filename_)
            #url_transform = endpoint_request_namenode.url.split('50070')
            
            #datanode_port = "50075"
            
            #endpoint_request_datanode = url_transform[0]+datanode_port+url_transform[1]
            
            #print("Datanode: ",endpoint_request_datanode)
            
            
            hdfs_saved_file = requests.Request('PUT', 
                                               url = response.url, 
                                               files = open("/home/skywalker/Desktop/flask-movie-bag/"+ filename_.split(" ")[1], "rb"))
            
            print(hdfs_saved_file.url)
            
            #print(hdfs_saved_file.status_code)
            
            #print(requests.get(endpoint_open_file))
          
        elif(hdfs_directory_status == "404"):
            
            print("Directory doesn't exists. Creating the directory under: ", hdfs_directory_folder_check)
            
            endpoint_open_dir = "http://skywalker-G7-7588:50070/webhdfs/v1/test/"+hdfs_directory_folder_check+"?op=MKDIRS"
            
            #files = {'upload_file': (hdfs_directory_folder_check, f)}
            
            hdfs_directory = requests.put(endpoint_open_dir)
            
            print("URL from hdfs", hdfs_directory.url)
            print("hdfs_directory_folder_check:  ", hdfs_directory_folder_check)
            print("hdfs_filename:  ",hdfs_filename)
            endpoint_open_file = "http://skywalker-G7-7588:50070/webhdfs/v1/test/"+hdfs_directory_folder_check+"/"+hdfs_filename+"?op=CREATE"
            
#            hdfs_saved_file = requests.put(endpoint_open_file, data = f)
            
            print(hdfs_saved_file.url)
            
            
      
        #print("File name: ", hdfs_directory_folder_check)
      
        
        
        
      
        #a = requests.post(endpoint_open)
        
        #print(a.url)
        
        #f.save(secure_filename(filename_))
        
        return 'file uploaded successfully'


@application.route('/movies/<id>')
def get_movie(id):
    movies = Data_create.objects.get(id=id).to_json()
    return Response(movies, mimetype="application/json", status=200)


#
#@application.route('/videofile')
#def view_file():
#   return redirect('hdfs://localhost:9000/user/hduser/pradeep.txt')
#	

application.run()






#
#
#
#
#
#
#
#my_data = open("/home/skywalker/Desktop/2020-06-20_145450.mp4", "rb")
#
#my_file = 'http://skywalker-G7-7588:50075/webhdfs/v1/test/testuser?op=MKDIR'
#
#
#a = requests.put(my_file, data=my_data)
#
#
#






























