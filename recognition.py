from __future__ import print_function
from flask import Flask, request
import src.delegates.getAllCamerasDelegate as ga
import src.delegates.addCameraDelegate as a
import src.delegates.removeCameraDelegate as r
import json

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace
app = Flask(__name__)


@app.route("/addCamera", methods=["POST"])
def addCamera():
    return a.addCameraDelegate.execute(request.json)


@app.route("/getAllCameras", methods=["GET"])
def getAllCameras():
    return json.dumps(list(ga.getAllCamerasDelegate.execute())), 200, {'ContentType': 'application/json'}


@app.route("/removeCamera/<address>", methods=["DELETE"])
def removeCamera(address):
    return r.removeCameraDelegate.execute(address)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
