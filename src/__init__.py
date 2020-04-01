from flask import Flask, request, Response
import io
import csv
import json

from . import functions as fn

app = Flask(__name__)
    
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
    # return Response(json.dumps(result), mimetype='application/json')

# /prediction?hour=<int:0-23>
# ? indicates that a parameter is optional
@app.route('/prediction', methods=['GET'])
def get_prediction():
    
    try:

        # Assume the input is correct, 0-23 integer value
        hour = int(request.args.get('hour'))
    
        ate = int(ate)
    
        return fn.PredictLR(hour, ate)

    except Exception as error:

        return str(error)

if __name__ == '__main__':  
    app.run(debug=True)
