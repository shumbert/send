from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    #return "<p>Hello, World!</p>"
    return "<p>Hello, " + name + "!</p>"

@app.route("/api/send", methods=['GET', 'PUT', 'POST'])
def send():
    pass

@app.route("/api/file", methods=['POST'])
def send():
    pass
