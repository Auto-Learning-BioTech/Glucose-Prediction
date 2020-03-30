from flask import Flask, request
import io
import csv

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"
    
@app.route("/salvador")
def salvador():
    return "Hello, Salvador"
    
@app.route("/datasets", methods=["POST"])
def post_datasets():
    f = request.files['data_file']

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    #print("file contents: ", file_contents)
    #print(type(file_contents))
    print(csv_input)
    for row in csv_input:
        print(row)
    return ""

if __name__ == "__main__":
    app.run(debug=True)
