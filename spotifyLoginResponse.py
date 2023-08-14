from flask import Flask, request
from threading import Thread

LOCAL_CALLBACK = "http://localhost:8888/callback"

app = Flask(__name__)

thread = None

# Flask queries routing:

@app.route("/")
def hola():
    return "Hola!"

@app.route("/callback")
def processSpotifyCallback():
    print("Received callback from Spotify")
    print(request.args.get('code'))
    print(request.args.get('state'))
    return "OK"

####

def start():
    thread = Thread(target = launch_flask)
    thread.start()


def launch_flask():
    app.run("0.0.0.0",port=8888)


if __name__ == '__main__':
    start()