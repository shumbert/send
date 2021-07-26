from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    #return "<p>Hello, World!</p>"
    return "<p>Hello, " + name + "!</p>"

@app.route("/api/send", methods=['GET', 'POST'])
def send():
    pass

@app.route("/api/file/<send>/<file>", methods=['POST'])
def file(send, file):
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
