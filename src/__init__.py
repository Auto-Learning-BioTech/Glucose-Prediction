from flask import Flask, request, Response
import io
import csv
import json

app = Flask(__name__)
    
# /datasets
# Required headers:
#   Content-Type: multipart/form-data
# Required form-data:
#   data_file key: String file
@app.route('/datasets', methods=['POST'])
def post_datasets():
    file = request.files['data_file'] # Expecting string only file
    stream = io.StringIO(file.stream.read().decode('UTF8'))
    lines = stream.getvalue().split('\n')
    result = []
    for line in lines:
        values = line.split('\t')
        if len(values) == 4: # Simple validation
            new_val = {}
            values = line.split('\t') 
            new_val['date'] = values[0]
            new_val['hour'] = int(values[1].split(':')[0])
            new_val['code'] = int(values[2])
            new_val['glucose'] = int(values[3])
            result.append(new_val)
    return Response(json.dumps(result), mimetype='application/json')

# /prediction?hour=<int:0-23>&ate=<?int:0|1>
# ? indicates that a parameter is optional
@app.route('/prediction', methods=['GET'])
def get_prediction():
    # Assume the input is correct, 0-23 integer value
    hour = int(request.args.get('hour'))
    ate = request.args.get('ate')
    if ate is None:
        # TODO: Handle prediction when ate is False
        return Response(json.dumps({ 'prediction': 'any type you see fit' }), mimetype='application/json')
    ate = int(ate)
    if ate == 0:
        # TODO: Handle prediction when ate is False
        return Response(json.dumps({ 'prediction': 'any type you see fit' }), mimetype='application/json')
    # TODO: Handle prediction when ate is True
    return Response(json.dumps({ 'prediction': 'any type you see fit' }), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
