import json
from collections import deque
import cv2
import threading
import os
from refactor.labels import Labels
from refactor.FrameExtractor import FrameExtractor
from refactor.labels import Labels
from refactor.Recognition import Recognition
from refactor.ImagePrediction import ImagePrediction

labels = Labels([])
f = FrameExtractor("../vid012.mp4", labels)
recognition = Recognition()

f.extract()