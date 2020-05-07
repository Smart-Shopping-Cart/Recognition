import os
import numpy as np
import torch
import json
import cv2
import time
from service.framesExtraction.ImagePrediction import ImagePrediction


path = ".." + os.path.sep + ".." + os.path.sep + "result" + os.path.sep + "predictions"


class Labels:
    # in case we want to self modify yhe labels arr we will send it
    # also we have default values
    def __init__(self, i_labels, i_recognition):
        self.image_predictions = []
        self.image_list = []
        self.recognition = i_recognition
        self.start_frame = 0
        self.end_frame = 0
        self.predictions = []
        self.timeBucket = {}
        self.times = []
        self.predicted_labels = []
        self.unknown = "unknown"
        self.model = torch.load(".." + os.path.sep + ".." + os.path.sep + "savedNet" + os.path.sep + "model.dat",
                                map_location=torch.device('cpu'))
        if len(i_labels) != 0:
            self.labels = i_labels
        else:
            # give default values
            self.labels = []
            red = "red ball"
            blue = "blue ball"
            yellow = "yellow ball"
            self.labels = ["MapleSyrup", "Mayonnaise", "NONE"]

    # get the predicted lable from the NN and append the label into labels array if the labels fits the requierments
    def insert_label(self, frame_to_insect, frame_number, i_direction):
        predicted_label = self.im_predict(frame_to_insect)
        if predicted_label in self.labels and predicted_label != "NONE":
            self.add_label(predicted_label, frame_number, time.perf_counter(), i_direction)
            return True
        # else:
        #     if len(self.labels) > 3 and self.labels[len(self.labels) - 3] != self.unknown:
        #         self.add_label(self.unknown, frame_number, time.perf_counter())
        #         return True

        return False

    def im_predict(self, img):
        """
        this function has static numbers need to be fixed
        :param img:
        :return lable:
        """
        self.model.eval()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
        if index1 == 0 and value - value1 < 0.055:
            index = index1
        elif index1 == 1 and value - value1 < 0.015:
            index = index1
        self.model.train()
        return names[index]

    def add_label(self, predicted_label, frame_number, i_time, i_direction):
        self.image_list.append((str(frame_number), str(i_direction)))
        self.predict(i_time, predicted_label, frame_number)
        self.predicted_labels.append((predicted_label, frame_number, i_time))



    def get_label_from_label_arr(self, label_index, is_first):
        if len(self.labels) > label_index:
            predicted_label = self.predicted_labels[label_index]
            if is_first:
                if predicted_label != self.unknown:
                    return self.predicted_labels[label_index]

    def dump_json(self):
        with open(path + os.path.sep + 'predictions.json', 'w') as outfile:
            json.dump(self.predicted_labels, outfile)

    def add_to_time_bucket(self, predicted_label):
        if predicted_label != "NONE":
            if len(self.timeBucket) == 0:
                for label in self.labels:
                    self.timeBucket[label] = 0
                return True
            else:
                self.timeBucket[predicted_label] += 1
                return False

    def add_to_times(self, i_time):
        if len(self.times) == 0:
            self.times.append(i_time)
            return True
        if i_time - self.times[len(self.times) - 1] > 0.4:
            return False
        else:
            self.times.append(i_time)
            return True

    def sum_and_reset_buckets(self, i_bool, predicted_label):
        if len(self.timeBucket) > 0 and self.timeBucket[max(self.timeBucket, key=self.timeBucket.get)] > 0:
            print(max(self.timeBucket, key=self.timeBucket.get))
            print(self.timeBucket)
            print(self.start_frame, self.end_frame)
            self.predictions.append(max(self.timeBucket, key=self.timeBucket.get))
            p = ImagePrediction(self.start_frame, self.end_frame, predicted_label, self.image_list)
            self.image_predictions.append(p)
            print(p.direction)
        if i_bool:
            self.times = []
            self.timeBucket = {}

    def predict(self, i_time, predicted_label, frame_number):
        if self.add_to_times(i_time):
            if self.add_to_time_bucket(predicted_label):
                self.start_frame = frame_number
        else:
            self.end_frame = frame_number
            self.sum_and_reset_buckets(True, predicted_label)
            if self.add_to_times(i_time):
                if self.add_to_time_bucket(predicted_label):
                    self.start_frame = frame_number

    def check_static_frame(self, i_time, frame_number):
        if len(self.times) > 0 and i_time - self.times[len(self.times) - 1] > 1:
            self.predict(i_time, "NONE", frame_number)
