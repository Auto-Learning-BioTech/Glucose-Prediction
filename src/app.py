from flask import Flask, request, Response, jsonify
import io
import csv
import json
import numpy as np
import functions as fn

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import messaging

app = Flask(__name__)

# #Firebase configuration
# cred = credentials.Certificate('glucose-prediction-4b002-firebase-adminsdk-7islk-3ff5c92f60.json')
# firebase_admin.initialize_app(cred)

#Device token
#dToken = "fYdcJpr8VJQ:APA91bE05mpSBrP0GN8ycKiAlk8-xK2Y1IbQLgvK8Wt2kJ4nRHEvNWE0h97WiPZQWPnDXN7oDGwn1oOBR_fUIdtYCGeF2nL4qKEoILKYz7rTFOBTIvtrV0WsFJTRI8QpoXHXrla1twCL"


@app.route('/')
def hello_world():
    a = np.array([[1, 1]])
    return str(a.shape[0])
# /datasets
# Required headers:
#   Content-Type: multipart/form-data
# Required form-data:
#   data_file key: String file
@app.route('/datasets', methods=['POST'])
def post_datasets():
    try:
        file = request.files['data_file']
        stream = io.StringIO(file.stream.read().decode('UTF8'))
        lines = stream.getvalue().split('\n')
        result = []
        for line in lines:
            values = line.split('\t')
            if len(values) == 4: # Simple validation
                new_val = {}
                values = line.split('\t')
                new_val['hour'] = int(values[1].split(':')[0])
                new_val['code'] = int(values[2])
                new_val['glucose'] = int(values[3])
                result.append(new_val)

        fn.TrainLR(result)
        return 'ok', 200
    except Exception as error:
        return str(error)

# /prediction?hour=<int:0-23>
# ? indicates that a parameter is optional
@app.route('/prediction', methods=['GET'])
def get_prediction():
    try:
        # Assume the input is correct, 0-23 integer value
        hour = int(request.args.get('hour'))
        return str(fn.PredictLR(hour))
    except Exception as error:
        return str(error)


@app.route('/insert', methods=['POST'])
def post_insert_data():
    try:
        hour = int(request.json.get('hour'))
        glucose = int(request.json.get('glucose'))
        day = int(request.json.get('day'))
        month = int(request.json.get('month'))
        filename = request.json.get('username')

        file = './intermediate_dataset/personal.csv'
        list = [month, day, hour, glucose]

        fn.append_list_as_row(file, list)

        return 'ok', 200
    except Exception as error:
        return str(error)

# #Future functionality
# #@app.route('/register', methods=['POST'])
# #def register_user

@app.route('/get/graph_data', methods=['GET'])
def get_graph_data():
    try:

        # Get csv name
        csv_name = request.args.get('name')
        # Get data to graph
        data = fn.get_data_from_csv(csv_name)
        response = {
            'data': data
        }

        return jsonify(response), 200

    except Exception as error:
        return str(error)


# #Sends a request to FCM to notify the device with the specified token
# @app.route('/status', methods=['GET'])
# def get_status():
#     try:
#         # Assume the input is correct, 0-23 integer value
#         hour = int(request.args.get('hour'))
#         dToken = str(request.args.get('token'))

#         status = fn.GetStatus(hour)

#         if(status == 'notify'):
#             notifyGlucose = messaging.Notification(title='Alerta', body='Checa tu nivel de glucosa')
#             message = messaging.Message(
#                 notification=notifyGlucose,
#                 token=dToken,
#             )

#             response = messaging.send(message)
#             print('Successfully sent message', response)

#         return status
#     except:
#         return str('error')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
