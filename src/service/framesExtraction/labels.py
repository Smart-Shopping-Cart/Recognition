import os
import numpy as np
import torch
import json


class Labels:
    # in case we want to self modify yhe labels arr we will send it
    # also we have default values
    def __init__(self, i_labels):
        self.predicted_labels = []
        self.unknown = "unknown"
        self.model = torch.load(
            ".." + os.path.sep + ".." + os.path.sep + ".." + os.path.sep + "savedNet" + os.path.sep + "model.dat")

        if len(i_labels) != 0:
            self.labels = i_labels
        else:
            # give default values
            self.labels = []
            red = "red ball"
            blue = "blue ball"
            yellow = "yellow ball"
            self.labels = [red, blue, yellow]

    # get the predicted lable from the NN and append the label into labels array if the labels fits the requierments
    def insert_label(self, frame_to_insect, frame_number):
        predicted_label = self.im_predict(frame_to_insect)
        if predicted_label in self.labels:
            self.add_label(predicted_label, frame_number)
            return True

        else:
            if len(self.labels) > 3 and self.labels[len(self.labels) - 3] != self.unknown:
                self.add_label(self.unknown)
                return True

        return False

    def im_predict(self, img):
        """
        this function has static numbers need to be fixed
        :param img:
        :return lable:
        """
        self.model.eval()
        image = np.array(img)
        image = image / 255.0  # simple normalization - just to maintain small numbers
        image = np.transpose(image, (2, 0, 1))
        tensor_image = ((torch.from_numpy(image)).unsqueeze(0))
        outputs = self.model(tensor_image.float())
        minValue, _ = outputs.min(1)
        outputs = (outputs + abs(minValue)) / 100
        outputs1 = outputs.clone()
        names = ["MapleSyrup", "Mayonnaise", "NONE"]
        value, index = outputs.max(1)
        if index == 2 and value < 0.1:
            outputs1[0][2] = 0
        value1, index1 = outputs1.max(1)
        if index1 == 0 and value - value1 < 0.05:
            index = index1
        elif index1 == 1 and value - value1 < 0.015:
            index = index1
        self.model.train()
        return names[index]

    def add_label(self, predicted_label, frame_number):
        self.predicted_labels.append(predicted_label, frame_number)

    @staticmethod
    def get_label_from_label_arr(self, label_index, is_first):
        if len(self.labels) > label_index:
            predicted_label = self.predicted_labels[label_index]
            if is_first:
                if predicted_label != self.unknown:
                    return self.predicted_labels[label_index]

    def dump_json(self):
        with open('predictions.txt', 'w') as outfile:
            json.dump(self.predicted_labels, outfile)
