from service.framesExtraction.FrameExtractor import FrameExtractor
from service.framesExtraction.Recognition import Recognition
from service.framesExtraction.labels import Labels

labels = Labels([])
f = FrameExtractor("../../../22.mp4", labels)
recognition = Recognition()

f.extract()
labels.dump_json()
