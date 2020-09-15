import threading
from threading import Thread
import cv2
from service.framesExtraction.StreamProcessor import StreamProcessor


class CameraManager:
    def __init__(self):
        self.workingCameras = {}  # {address:ThreadId}
        self.stopWorking = []

    def validateCamera(self, address):
        if address in self.workingCameras.keys():
            return False, None
        if address != "0":
            rtspAddress = "rtsp://" + address + "/"
            httpAddress = "http://" + address + "/"
        else:
            rtspAddress = 0
            httpAddress = 0
        camera = cv2.VideoCapture(rtspAddress)
        if camera.isOpened():
            return True, camera
        camera = cv2.VideoCapture(httpAddress)
        if camera.isOpened():
            return True, camera
        else:
            return False, None

    def startStream(self, address, camera):
        thread = Thread(target=self.recognize, kwargs={'camera': camera, 'address': address}, daemon=True)
        thread.start()
        self.workingCameras[address] = thread.ident

    def stopStream(self, address):
        if address in self.workingCameras.keys():
            self.stopWorking.append(self.workingCameras[address])

    def recognize(self, camera, address):
        id = threading.get_ident()
        processor = StreamProcessor(camera, address)
        print("camera " + str(address) + " started streaming")
        while camera.isOpened():
            if self.stopWorking.count(id) > 0:
                self.stopWorking.remove(id)
                self.workingCameras.pop(address)
                camera.release()
                print("camera " + str(address) + " has stopped")
                raise SystemExit()
            processor.capture()


manager = CameraManager()
