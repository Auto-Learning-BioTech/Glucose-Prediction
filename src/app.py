from flask import Flask, request, Response, jsonify
from werkzeug.utils import secure_filename
import datetime
from datetime import timedelta, datetime

import os
import io
import csv
import json
import numpy as np
import functions as fn
import pytz
from tzlocal import get_localzone

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import firestore


app = Flask(__name__)

#Configure path to directory to receive files
UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cred = None

#Control file input for specific types of files
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#joins day, month and year into one string
def convert_date(year, month, day, hour):
    new_hour = ""
    new_day = ""
    new_month = ""
    new_date = ""
    
    if(len(str(day)) == 1):
        new_day = "0" + str(day)
    else:
        new_day = str(day)

    if(len(str(month)) == 1):
        new_month = "0" + str(month)
    else:
        new_month = str(month)

    if(len(str(hour)) == 1):
        new_hour = "0" + str(hour)
    else:
        new_hour = str(hour)

    new_date = str(year) + new_month + new_day + new_hour
    return new_date

@app.route('/')
def hello_world():
    a = np.array([[1, 1]])
    return str(a.shape[0])

#Initialize firebase configuration with JSON credentials
@app.route('/initialize_firebase', methods=['POST'])
def initializeFirebase():
    try:
        credJsonFile = request.files['credentials']

        if credJsonFile and allowed_file(credJsonFile.filename):
            filename = secure_filename(credJsonFile.filename)
            credJsonFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cred = credentials.Certificate(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        firebase_admin.initialize_app(cred)

        return("Initialized")
    except Exception as error:
        return str(error)

#Checks if the user exists
@app.route('/login_check', methods=['POST'])
def login_check():
    try:
        username = request.form['username']

        db = firestore.client()
        doc = db.collection('users').document(username).get()

        if(doc.exists):
            return 'existent'
        else:
            return 'non existent'
    except Exception as error:
        return str(error)

#Register new user in DB
@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        username = request.form['username']
        device_token = request.form['device_token']

        db = firestore.client()

        doc_ref = db.collection(u'users').document(username)
        doc = doc_ref.get()

        if(doc.exists):
            return "user already exists"
        else:
            doc_ref = db.collection(u'users').document(username)
            doc_ref.set({
                    'device_token':device_token,
                    'exp_arr' : [0]
                })

            return "registered"
    except Exception as error:
        return str(error)

#Update user device token
@app.route('/update_device_token', methods=['POST'])
def update_device_token():
    try:
        username = request.form['username']
        device_token = request.form['device_token']

        db = firestore.client()
        doc_ref = db.collection(u'users').document(username)
        doc_ref.update({u'device_token':device_token})

        return 'updated'
    except Exception as error:
        return str(error)

@app.route('/insert_json_db', methods=['POST'])
def insert_json_db():
    try:
        user = request.json.get('username')
        data = request.json.get('data')

        db = firestore.client()
        doc_ref = db.collection(u'users').document(user)
        doc = doc_ref.get()

        if(doc.exists):
            doc_dict = doc.to_dict()
            exp_arr = doc_dict['exp_arr']
            exp_arr = fn.RetrainPoly(exp_arr,data)
            doc_ref.update({u'exp_arr':exp_arr})
        
        for obj in data:
            year = obj.get('year')
            month = obj.get('month')
            day = obj.get('day')
            hour = obj.get('hour')
            level = obj.get('level')

            converted_date = convert_date(year, month, day, hour)
            doc_ref = db.collection(u'data').document(converted_date + user)
            doc_ref.set(
                {
                    u'year': year,
                    u'month' : month,
                    u'day' : day,
                    u'hour' : hour,
                    u'glucose_level' : level,
                    u'username_fk' : user,
                    u'datetime' : datetime(int(year), int(month), int(day), int(hour), 0, 0, tzinfo=get_localzone())
                }
            )

        return 'ok', 200
    except Exception as error:
        return str(error)

#Insert new meassures via single value
@app.route('/new_meassurement', methods=['POST'])
def new_meassurement():
    try:
        user = request.json.get('username')
        year = request.json.get('year')
        month = request.json.get('month')
        day = request.json.get('day')
        hour = request.json.get('hour')
        level = request.json.get('level')

        converted_date = convert_date(year, month, day, hour)

        db = firestore.client()
        doc_ref = db.collection(u'data').document(converted_date + user)
        doc_ref.set(
            {
                u'year': year,
                u'month' : month,
                u'day' : day,
                u'hour' : hour,
                u'glucose_level' : level,
                u'username_fk' : user,
                u'datetime' : datetime(year, month, day, hour, 0, 0, tzinfo=get_localzone())
            }
        )

        return 'ok'

    except Exception as error:
        return str(error)

#Set user specific exponents in DB used for ML Model
@app.route('/set_user_model', methods=['POST'])
def set_user_model():
    try:
        exp_arr = request.json.get('exp_arr')
        username = request.json.get('username')

        db = firestore.client()
        doc_ref = db.collection(u'users').document(username)
        doc_ref.update({u'exp_arr':exp_arr})

        return 'exp_arr updated'
    except Exception as error:
        return str(error)

#Predict for specific user
@app.route('/user_predict', methods=['POST'])
def user_predict():
    try:
        username = request.form['username']
        hour = request.form['hour']

        db = firestore.client()
        doc = db.collection(u'users').document(username).get()

        if(doc.exists):
            doc_dict = doc.to_dict()
            exp_arr = doc_dict['exp_arr']
            device_token = doc_dict['device_token']

            result = fn.Polypredict(exp_arr,hour)
            level = result['level']

            resStr = 'Se predice nivel: ' + level + ' mg/dl'

            message = messaging.Message(
                data={
                    'title': 'Alerta de Glucosa',
                    'body': resStr
                },
                token=device_token,
            )

            response = messaging.send(message)

            return jsonify(result)
        else:
            return('user non existent')
            
    except Exception as error:
        return str(error)

#Get history, gets the records of the last 'n' days
@app.route('/get_history', methods=['POST'])
def get_history():
    try:
        username = request.form["username"]
        days = request.form["days"]

        tzone = get_localzone()

        now = datetime.now(tz=tzone)
        delta = timedelta(days=int(days))
        start_date = now - delta

        db = firestore.client()
        query = db.collection (u'data').where(u'username_fk', u'==', username).where(u'datetime', u'>=', start_date).stream()

        docs_dict = []

        for doc in query:
            docs_dict.append(doc.to_dict())

        json_response = jsonify(docs_dict)

        return json_response
    except Exception as error:
        return str(error)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
