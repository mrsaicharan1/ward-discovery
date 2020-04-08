#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from helpers import generate_uuid
from forms import *
import os
import bcrypt
import boto3
from boto3.dynamodb.conditions import Key, Attr
from batch_write import batch_write_ddb
import traceback
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


@app.route('/find-wards', methods=['POST','GET'])
def find_wards():
    table = dynamodb.Table('provider')


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
            wards_availble = int(request.form['wards_available'])
            # ID generation for wards
            wards_dict = dict()
            for ward in range(wards_availble):
                ward_id = generate_uuid()
                wards_dict[ward_id] = 1
            provider_id = generate_uuid()
            table.put_item(
            Item={
                    'name': request.form['name'],
                    'provider_id': provider_id,
                    'password': hashed_password,
                    'email': request.form['email'],
                    'address': request.form['address'],
                    'wards': wards_dict
                }
            )
            # ward ids pushed to DDB table
            try:
                batch_write_ddb(provider_id ,wards_dict.keys())
            except Exception as e:
                print('DDB Batch write failed due to {}'.format(e))
                

            print('Signup Successful')
    return render_template('forms/provider_signup.html')

@app.route('/seeker-signup', methods=['POST','GET'])
def seeker_signup():
    if request.method == 'POST':
        table = dynamodb.Table('seeker')
        try:
            user = table.get_item(
                Key = {
                    'email': request.form['email'],
                }
            )
            flash('Account already exists. Please log in')
        except Exception as e:
            table = dynamodb.Table('seeker')
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10))
            table.put_item(
            Item={
                    'name': request.form['name'],
                    'seeker_id': generate_uuid(),
                    'password': hashed_password,
                    'email': request.form['email'],
                    'address': request.form['address'],
                }
            )

            print('Signup Successful')
    return render_template('forms/seeker_signup.html')


@app.route('/seeker-login', methods=['POST','GET'])
def seeker_login():
    table = dynamodb.Table('seeker')
    if request.method == 'POST':
        try:
            response = table.scan(
                FilterExpression=Attr('email').eq(request.form['email'])
            )
            user_record = response['Items'][0]
            print(user_record)
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), user_record['password'].value):
                session['email'] = request.form['email']
                print("login successful")
        except Exception as e:
            return traceback.format_exc()


    return render_template('forms/seeker_login.html')
    

@app.route('/provider-login', methods=['POST', 'GET'])
def provider_login():
    table = dynamodb.Table('provider')
    if request.method == 'POST':
        try:
            response = table.scan(
                FilterExpression=Attr('email').eq(request.form['email'])
            )
            user_record = response['Items'][0]
            print(user_record)
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), user_record['password'].value):
                session['email'] = request.form['email']
                print("login successful")
        except Exception as e:
            return traceback.format_exc()


    return render_template('forms/provider_login.html')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)