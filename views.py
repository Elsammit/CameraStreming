from django.shortcuts import render
from django.http import HttpResponse
import cv2
from django.http import StreamingHttpResponse
from testProject.settings import BASE_DIR

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture("http://192.168.11.2:8080/?action=stream")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        cascade_path = BASE_DIR + "\haarcascade_frontalface_default.xml"

        success, image = self.video.read()

        gry_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(cascade_path)

        facerect = cascade.detectMultiScale(gry_img,scaleFactor=1.5,minNeighbors=2,minSize=(60,60))

        rectange_color = (255,0,0)

        if len(facerect) > 0:
            for rect in facerect:
                cv2.rectangle(image,tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),rectange_color,thickness=2)
        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def index(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')