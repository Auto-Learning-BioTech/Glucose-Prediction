from flask import Flask, request
import io
import csv
import json

app = Flask(__name__)
    
@app.route('/datasets', methods=['POST'])
def post_datasets():
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
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)
