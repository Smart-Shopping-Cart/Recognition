# Frame Extractor
in order to only extract relevant frames from a video stream perform the following ections:

1. use  FrameExtractor.py
2. provide the path of the output of this program (path = "C:" + os.path.sep + "Users" + os.path.sep + "Aviram" + os.path.sep + \
       "PycharmProjects" + os.path.sep + "helloWorld" + os.path.sep + "Result")
3. create a FrameExtractor instance f = FrameExtractor(video_stream, array of labels/emptyArr)
    for example f = FrameExtractor("C:\Users\Aviram\PycharmProjects\helloWorld\vid030.mp4", [])
4. use the f.extract() method



#further specifiecs:
1. in this time you need to comment line ("if Labels.insert_labels()") if exists
2. some time you need to rotate the frames (if the automation doesnt work)
 
    2.a play with comment and un comment this line :( frame1 = cv2.rotate(frame1/2, cv2.ROTATE_90_CLOCKWISE))