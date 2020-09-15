import copy
import time
import cv2
import numpy as np
import torch
import os
from gateways.cartHandlingApi import CartHandlingApi


class StreamProcessor:
    def __init__(self, cap, cameraAddress):
        self.cap = cap
        self.cameraAddress = cameraAddress
        self.lastImage = None
        self.lastLocation = None
        self.model = torch.load("savedNet" + os.path.sep + "model.dat",
                                map_location=torch.device('cpu'))
        self.names = ["MapleSyrup", "Mayonnaise", "NONE"]
        self.contextNameCountConst = {"MapleSyrup": 0, "Mayonnaise": 0, "NONE": 0}
        self.contextDirectionCountConst = {"MapleSyrup": {"IN": 0, "OUT": 0, "STILL": 0, },
                                           "Mayonnaise": {"IN": 0, "OUT": 0, "STILL": 0, },
                                           "NONE": {"IN": 0, "OUT": 0, "STILL": 0, }, }
        self.contextNameCount = copy.deepcopy(self.contextNameCountConst)
        self.contextDirectionCount = copy.deepcopy(self.contextDirectionCountConst)
        self.contextSwitchThreshHold = 0.4
        self.contextCaptureThreshHold = 10
        self.clockTick = None
        self.cartHandlingApi = CartHandlingApi()

    def capture(self):
        ret, Image = self.cap.read()
        Image = cv2.rotate(Image, cv2.ROTATE_90_CLOCKWISE)
        if self.lastImage is None:
            self.lastImage = Image
        isContoursGood, x, y, w, h = self.validateContours(Image)
        self.lastImage = Image
        if isContoursGood:
            direction = self.getDirection(x, y, h)
            imageToPredict = cv2.medianBlur(Image, ksize=3)
            imageToPredict = cv2.resize(imageToPredict, (128, 128))
            self.predictAndHandleGoodFrame(imageToPredict, direction)
        else:
            self.predictAndHandleBadFrame()

    def getDirection(self, x, y, h):
        if self.lastLocation is None:
            self.lastLocation = (x, (y + h))
        location = (x, (y + h))

        if location[1] - self.lastLocation[1] > 0:
            self.lastLocation = location
            return "IN"
        elif location[1] - self.lastLocation[1] < 0:
            self.lastLocation = location
            return "OUT"
        else:
            self.lastLocation = location
            return "STILL"

    def validateContours(self, frame):
        diff = cv2.absdiff(self.lastImage, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)
            if not ((y + h) > 650 or cv2.contourArea(c) < 2500):
                return True, x, y, w, h
        return False, None, None, None, None

    def predictAndHandleBadFrame(self):
        if self.isContextFinished():
            if sum(self.contextNameCount.values()) > self.contextCaptureThreshHold:
                self.sendResultsAndResetContext()
            else:
                self.resetContext()

    def predictAndHandleGoodFrame(self, image, direction):
        label = self.predictLabel(image)
        if label is not "NONE":
            if self.isContextFinished():
                if sum(self.contextNameCount.values()) > self.contextCaptureThreshHold:
                    self.sendResultsAndResetContext()
                else:
                    self.resetContext()
            self.contextNameCount[label] += 1
            self.contextDirectionCount[label][direction] += 1
            self.clockTick = time.perf_counter()

    def sendResultsAndResetContext(self):
        contextLabel = max(self.contextNameCount, key=self.contextNameCount.get)
        contextDirection = max(self.contextDirectionCount[contextLabel],
                               key=self.contextDirectionCount[contextLabel].get)
        if contextDirection is "IN":
            print(self.cameraAddress, contextLabel, contextDirection)
            self.cartHandlingApi.addProduct(self.cameraAddress, contextLabel)
        if contextDirection is "OUT":
            print(self.cameraAddress, contextLabel, contextDirection)
            self.cartHandlingApi.removeProduct(self.cameraAddress, contextLabel)
        self.resetContext()

    def resetContext(self):
        self.contextNameCount = copy.deepcopy(self.contextNameCountConst)
        self.contextDirectionCount = copy.deepcopy(self.contextDirectionCountConst)

    def isContextFinished(self):
        if self.clockTick is None:
            self.clockTick = time.perf_counter()
        currentTime = time.perf_counter()
        if currentTime - self.clockTick > self.contextSwitchThreshHold:
            return True
        return False

    def predictLabel(self, image):
        self.model.eval()
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.array(img)
        image = image / 255.0
        image = np.transpose(image, (2, 0, 1))
        tensor_image = ((torch.from_numpy(image)).unsqueeze(0))
        outputs = self.model(tensor_image.float())
        minValue, _ = outputs.min(1)
        outputs = (outputs + abs(minValue)) / 100
        outputs1 = outputs.clone()
        value, index = outputs.max(1)
        if index == 2 and value < 0.1:
            outputs1[0][2] = 0
        value1, index1 = outputs1.max(1)
        if index1 == 0 and value - value1 < 0.055:
            index = index1
        elif index1 == 1 and value - value1 < 0.015:
            index = index1
        self.model.train()
        return self.names[index]
