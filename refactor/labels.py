class Labels:
    # in case we want to self modify yhe labels arr we will send it
    # also we have default values
    def __init__(self, i_labels):
        self.predicted_labels = []
        self.unknown = "unknown"

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
    def insert_label(self, frame_to_insect):
        predicted_label = self.get_yoni_labels(frame_to_insect)
        if predicted_label in self.labels:
            self.add_label(predicted_label)
            return True

        else:
            if len(self.labels) > 3 and self.labels[len(self.labels) - 3] != self.unknown:
                self.add_label(self.unknown)
                return True

        return False

    def get_yoni_labels(self, frame_to_insect):
        return "blue ball"

    def add_label(self, predicted_label):
        self.predicted_labels.append(predicted_label)

    @staticmethod
    def get_label_from_label_arr(self, label_index, is_first):
        if len(self.labels) > label_index:
            predicted_label = self.predicted_labels[label_index]
            if is_first:
                if predicted_label != self.unknown:
                    return self.predicted_labels[label_index]