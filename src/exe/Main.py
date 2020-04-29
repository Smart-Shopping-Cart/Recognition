from src.service.framesExtraction.FrameExtractor import FrameExtractor
from src.service.framesExtraction.Recognition import Recognition
from src.service.framesExtraction.labels import Labels

labels = Labels([])
f = FrameExtractor("../vid012.mp4", labels)
recognition = Recognition()

f.extract()
labels.dump_json()
