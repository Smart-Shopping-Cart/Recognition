from service.framesExtraction.FrameExtractor import FrameExtractor
from service.framesExtraction.Recognition import Recognition
from service.framesExtraction.labels import Labels
import threading


labels = Labels([])
f = FrameExtractor("../../resources/vid22.mp4", labels)
recognition = Recognition(labels)

f.extract()
f.calculate_labels()
labels.dump_json()
