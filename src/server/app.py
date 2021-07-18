from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    #return "<p>Hello, World!</p>"
    return "<p>Hello, " + name + "!</p>"

@app.route("/api/send")
def hello_world():
    pass
