from src.service.framesExtraction.ImagePrediction import ImagePrediction
from src.service.framesExtraction.labels import Labels


class Recognition:
    def __init__(self, i_labels):
        self.labels = i_labels

    @classmethod
    def do(cls):
        print("do")

    def recognize(self):
        predictions = []
        # start_counting represent the starting index of the predicted image
        start_counting = 0
        not_equal = 0
        counter = 1

        # use Recognize func (get_labels) to identify the predicted label and skip an unknown label if necessary
        predicted_label = Labels.get_label_from_label_arr(self.labels, start_counting, True)

        while True:
            if not_equal > 1:
                new_start_counting = start_counting + counter - not_equal
                if (new_start_counting - 1) - start_counting + 1 >= 2:
                    predictions.append(ImagePrediction(start_counting, new_start_counting - 1, predicted_label))
                start_counting += new_start_counting
                predicted_label = Labels.get_label_from_label_arr(self.labels, start_counting, False)
                not_equal = 0
                counter = 1

            predicted_label2 = Labels.get_label_from_label_arr(self.labels, start_counting + counter, False)
            if predicted_label == predicted_label2:
                not_equal = 0
            else:
                not_equal += 1

            counter += 1
