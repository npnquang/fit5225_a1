from flask import Flask, request, jsonify

print(__name__)
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!<p>"


@app.route("/detect")
def detect():
    data = request.get_json

if __name__ == "__main__":
    app.run(debug=True, threaded=True)