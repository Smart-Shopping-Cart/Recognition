import json
from collections import deque
import cv2
import threading
import os
from FrameExtractor import FrameExtractor
from labels import Labels
from Recognition import Recognition

labels = Labels([])
f = FrameExtractor("C:/Users/Aviram/PycharmProjects/helloWorld/vid21.mp4", labels)
recognition = Recognition()

f.extract()
labels.dump_json()