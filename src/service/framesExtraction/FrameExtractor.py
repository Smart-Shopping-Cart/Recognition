import json
from collections import deque
import cv2
import threading
import os

# path of resulted extracted frames
from src.service.framesExtraction.labels import Labels

path = "C:" + os.path.sep + "Users" + os.path.sep + "Aviram" + os.path.sep + \
       "PycharmProjects" + os.path.sep + "helloWorld" + os.path.sep + "Result"


class FrameExtractor:
    # give the Ctor the video path ip / stream
    def __init__(self, video_path, i_Labels):
        self.video_stream_path = video_path
        self.image_list = []
        self.frame_counter = 0
        self.image_number = 0
        self.Labels = i_Labels

    def extract(self):
        cap = cv2.VideoCapture(self.video_stream_path)
        cap.set(3, 480)
        cap.set(4, 848)
        pts = deque(maxlen=64)

        ret, frame1 = cap.read()
        frame1 = cv2.rotate(frame1, cv2.ROTATE_90_CLOCKWISE)
        ret, frame2 = cap.read()
        frame2 = cv2.rotate(frame2, cv2.ROTATE_90_CLOCKWISE)

        while cap.isOpened():
            # finds the frame contours based on the diff between the current frame and the prev frame
            contours, _ = self.find_contours(frame1, frame2)
            # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

            self.identify_and_write(contours, frame1, pts, self.image_list)

            cv2.imshow("feed", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()
            if ret is False:
                break
            frame2 = cv2.rotate(frame2, cv2.ROTATE_90_CLOCKWISE)

            if cv2.waitKey(40) == 27:
                break

        with open('output.txt', 'w') as outfile:
            json.dump(self.image_list, outfile)

        cv2.destroyAllWindows()
        cap.release()

    def find_contours(self, frame_1, frame_2):
        diff = cv2.absdiff(frame_1, frame_2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        return cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def identify_and_write(self, i_contours, i_frame1, i_pts, i_imagelist):
        self.frame_counter
        self.image_number
        if len(i_contours) > 0:
            # find the largest contour in the mask, then use
            # the following filters to get the correct frames
            skip = False
            c = max(i_contours, key=cv2.contourArea)

            (x, y, w, h) = cv2.boundingRect(c)
            if (y + h) > 650:
                skip = True
            # if (y + h) < 100:
            #     skip = True
            if cv2.contourArea(c) < 2500:
                skip = True
            # if cv2.contourArea(c) > 20000:
            #     skip = True

            if not skip:
                i_pts.appendleft((x, (y + h)))
                # crop_img = i_frame1[:, :600]
                crop_img = cv2.medianBlur(i_frame1, ksize=5)
                crop_img = cv2.resize(crop_img, (128, 128))
                self.frame_counter += 1
                direction = ""
                if len(i_pts) > 1 and self.frame_counter % 2 == 0:
                    if i_pts[0][1] - i_pts[1][1] > 0:
                        direction = -1
                    if i_pts[0][1] - i_pts[1][1] < 0:
                        direction = 1

                    if Labels.insert_label(self.Labels, crop_img):
                        self.image_number += 1
                        i_imagelist.append((str(self.image_number), str(direction)))
                        cv2.imwrite(path + "/%d" % self.image_number + '.jpg', crop_img)
                    else:
                        print("this frame is not good")

                    # ==============================================
                    # activate recognize

            cv2.rectangle(i_frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(i_frame1, (x, y + h), 5, (0, 0, 255), -1)
