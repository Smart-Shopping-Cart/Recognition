from src.service.framesExtraction.ImagePrediction import ImagePrediction
from src.service.framesExtraction.labels import Labels


class Recognition:
    def __init__(self):
        self.predictions = []

    def recognize(self, start_frame, end_frame, predicted_label, image_list):
        self.predictions.append(ImagePrediction(start_frame, end_frame, predicted_label, image_list))
        print(self.predictions[0])


