from flask import Flask, render_template

from src.delegates.addCameraDelegate import addCameraDelegate
from src.delegates.getAllCamerasDelegate import getAllCamerasDelegate
from src.delegates.removeCameraDelegate import removeCameraDelegate

app = Flask(__name__)


@app.route("/")
def index():
    return 'blank'


@app.route("/addCamera")
def addCamera():
    return addCameraDelegate.execute()


@app.route("/removeCamera")
def removeCamera():
    return removeCameraDelegate.execute()


@app.route("/getAllCameras")
def getAllCameras():
    return getAllCamerasDelegate.execute()


if __name__ == "__main__":
    app.run(debug=True)
