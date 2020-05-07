from service.framesExtraction.FrameExtractor import FrameExtractor
from service.framesExtraction.Recognition import Recognition
from service.framesExtraction.labels import Labels
import threading

recognition = Recognition()
labels = Labels([], recognition)
f = FrameExtractor("../../resources/vid22.mp4", labels)

f.extract()
labels.dump_json()
