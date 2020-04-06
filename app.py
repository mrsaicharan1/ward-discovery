#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from helpers import generate_uuid
from forms import *
import os
import bcrypt
import boto3

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')


dynamodb = boto3.resource('dynamodb')
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/provider-signup', methods=['POST','GET'])
def provider_signup():
    if request.method == 'POST':
        table = dynamodb.Table('provider')
        try:
            user = table.get_item(
                Key = {
                    'email': request.form['email'],
                }
            )
            flash('Account already exists. Please log in')
        except Exception as e:
            table = dynamodb.Table('provider')
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10))
            table.put_item(
            Item={
                    'name': request.form['name'],
                    'provider_id': generate_uuid(),
                    'password': hashed_password,
                    'email': request.form['email'],
                    'address': request.form['address'],
                }
            )
            print('Signup Successful')
    return render_template('forms/signup.html')


@app.route('/seeker/login')
def seeker_login():
    pass

@app.route('/provider/login')
def provider_login():
    if request.method == 'POST':
        pass


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)