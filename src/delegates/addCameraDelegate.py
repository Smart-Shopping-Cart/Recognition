from service.camerasManager.CameraManager import manager
import json


class addCameraDelegate:
    def __init__(self):
        pass

    @classmethod
    def execute(cls, cameraObj):
        ret, camera = manager.validateCamera(cameraObj["ip"])
        if ret:
            manager.startStream(cameraObj["ip"], camera)
            return json.dumps({'massage': "pair successfully"}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'massage': "cannot bind to camera"}), 500, {'ContentType': 'application/json'}