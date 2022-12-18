import boto3
import json
from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread


global capture
capture=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
#net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camera
    global capture
    while True:
        success, frame = camera.read() 
        if success:  
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)       
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

account_id = "ASIAWIM27RKEBOT7NZ37"
account_key = "ozS+KZZHpNXUsM1m1+tSdXR3rF1OMG1O6xIQoQx+"
aws_token="FwoGZXIvYXdzEBUaDLKIL/CKTGKzxmrX/CLPAU4WObxHpqz6oQbvyEp4VS1xuf5EalarM47hzT7mBsQVj+mpOy1RnjUn2voZSlCNnIdOBC8WvSJF5e/vzbTFnlnm39F73nEMYyULIEKz8/UQNiKCtUeqBiLL55mF7DqcNmRbpxm51OwtC7lrX0JtIULZlprGOZiGCbONgQOUjBoiZhquLW3rKjjxYYXN0KB8PRyAGM8zGoDZZaDVVoKyITobVW7te1EujigtpW+DXIsZMuZml5xfkDve9DFk8pmQ3+Wxu4DnGwAsKULGUydkyCjglPqcBjItMYuAncxrqFH9eXNDL6jcmT/h66CoGnXafaQvOta5JO0+h02nDWDR22El0QRs"
def client():
    global account_id
    global account_key
    global account_token
    print(account_id, account_key)
    client = boto3.client("textract", aws_access_key_id=account_id,
                          aws_secret_access_key=account_key,
                          aws_session_token = aws_token,
                          region_name='us-east-1')
    return client
app = Flask(__name__)

@ app.route("/", methods=["GET"])
def main():
    extractedText = ""
    responseJson = {

        "text": extractedText
    }
    return render_template("test.html", jsonData=json.dumps(responseJson))

@ app.route("/extracttext", methods=["POST"])
def extractImage():
    file = request.files.get("filename")
    binaryFile = file.read()
    textractclient = client()
    response = textractclient.detect_document_text(
        Document={
            'Bytes': binaryFile
        }
    )
    extractedText = ""
    for block in response['Blocks']:
        if block["BlockType"] == "LINE":
            extractedText = extractedText+block["Text"]+" "
    responseJson = {

        "text": extractedText
    }
    print(responseJson)
    return render_template("test.html", jsonData=json.dumps(responseJson))


@app.route('/camera', methods=["POST"])
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1     
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

camera.release()
 

