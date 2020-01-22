from flask import Flask
app = Flask (__name__)
@app.route("/")

def hello():
    return "Hello World !"

if __name__ = " ___main___":
    app.run(host="localhost", port = 8889, debug = True)    