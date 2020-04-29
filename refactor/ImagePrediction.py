import json

class ImagePrediction:
    def __init__(self, starting_index, end_index, predicted_image):
        self.starting_index = starting_index
        self.end_index = end_index
        self.predicted_image = predicted_image
        self.direction = self.find_direction(starting_index, end_index)

    def percentage(self, part, whole):
        return 100 * float(part) / float(whole)

    def find_direction(self, i_start, i_end):
        with open('output.txt') as json_file:
            data = json.load(json_file)

        count_south = 0
        count_north = 0

        for (num, direction) in data:
            if i_start <= int(num) <= i_end:
                if int(direction) == 1:
                    count_north += 1
                else:
                    count_south += 1

        north_percent = self.percentage(count_north, i_end - i_start + 1)
        south_percent = self.percentage(count_south, i_end - i_start + 1)

        if north_percent > 60:
            return 1, True
        elif south_percent > 60:
            return -1, True
        else:
            if north_percent > south_percent:
                return 1, False
            else:
                return -1, False
