from labels import Labels
from ImagePrediction import ImagePrediction


class Recognition:

    @classmethod
    def recognize(cls):
        predictions = []
        # start_counting represent the starting index of the predicted image
        start_counting = 0
        not_equal = 0
        counter = 1

        # use Recognize func (get_labels) to identify the predicted label and skip an unknown label if necessary
        predicted_label = Labels.get_label_from_label_arr(start_counting)

        while True:
            if not_equal > 1:
                new_start_counting = start_counting + counter - not_equal
                if (new_start_counting - 1) - start_counting + 1 >= 2:
                    predictions.append(ImagePrediction(start_counting, new_start_counting - 1, predicted_label))
                start_counting += new_start_counting
                predicted_label = Labels.get_label_from_label_arr(start_counting)
                not_equal = 0
                counter = 1

            predicted_label2 = Labels.get_label_from_label_arr(start_counting + counter)
            if predicted_label == predicted_label2:
                not_equal = 0
            else:
                not_equal += 1

            counter += 1
