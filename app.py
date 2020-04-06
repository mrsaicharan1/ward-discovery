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
db = SQLAlchemy(app)

dynamodb = boto3.resource('dynamodb')
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        if request.form['user_type'] == 'Seeker':
            table = dynamodb.Table('Users')
            user = table.get_item(
                key = {
                    'email': request.form.data,
                }
            )
            if user is None:
                hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10))
                table.put_item(
                Item={
                        'hospital_name': request.form['hospital_name'],
                        'hospital_id': generate_uuid(),
                        'password': hashed_passwords,
                        'email': request.form['email'],
                        'address': request.form['address'],
                    }
                )
                flash('Signup Successful')
        elif request.form['user_type'] == 'Provider':
            table = dynamodb.Table('Providers')
            user = table.get_item(
                key = {
                    'email': request.form.data,
                }
            )
            if user is None:
                hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10))
                table.put_item(
                Item={
                        'hospital_name': request.form['hospital_name'],
                        'hospital_id': generate_uuid(),
                        'password': hashed_passwords,
                        'email': request.form['email'],
                        'address': request.form['address'],
                    }
                )
                flash('Signup Successful')
            else:
                flash('This account already exists')
    return render_template('forms/signup.html')


@app.route('/seeker/login')
def seeker_login():
    pass

@app.route('/provider/login')
def provider_login():
    if request.method == 'POST':
        pass


# @app.route('/login')
# def login():
#     form = LoginForm(request.form)
#     return render_template('forms/login.html', form=form)


# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
