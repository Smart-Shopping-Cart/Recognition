from service.camerasManager.CameraManager import manager
import json


class removeCameraDelegate:
    def __init__(self):
        pass

    @classmethod
    def execute(cls, address):
        manager.stopStream(address)
        return json.dumps({'massage': "camera removed successfully"}), 200, {'ContentType': 'application/json'}