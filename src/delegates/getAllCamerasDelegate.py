from service.camerasManager.CameraManager import manager


class getAllCamerasDelegate:
    def __init__(self):
        pass

    @classmethod
    def execute(cls):
        return manager.workingCameras.keys()
