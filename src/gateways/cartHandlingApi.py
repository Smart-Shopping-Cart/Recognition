import requests


class CartHandlingApi:
    def __init__(self):
        pass

    def addProduct(self, cameraId, productId):
        requests.post("http://127.0.0.1:8080/addProduct/"+cameraId+"/"+productId)

    def removeProduct(self, cameraId, productId):
        requests.post("http://127.0.0.1:8080/removeProduct/"+cameraId+"/"+productId)