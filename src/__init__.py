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
            # TODO: Change this Jorge
            new_val = {}
            values = line.split('\t')
            new_val['date'] = values[0]
            new_val['hour'] = values[1]
            new_val['code'] = values[2]
            new_val['glucose'] = values[3]
            result.append(new_val)
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)
