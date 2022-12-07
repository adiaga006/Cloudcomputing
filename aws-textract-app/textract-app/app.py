from flask import render_template, Flask, request
import boto3
import json
account_id = "ASIAWIM27RKEGAXZ5S7V"
account_key = "rG3chr52yy2pt9ymuDUyYp5o5ldFCGgNcNZVzbNh"
aws_token="FwoGZXIvYXdzEBQaDC4ukJtxlnf4O36FNSLPAQy1Kpce+F+chc0fIVR6J12hGiSEbkUV2b3MioJnWmQ4Z+P3kznzTBgvOXleCDTwqzgA59afkMdxNyvtgAnpW42ghdJif5XQlNI6xnJrA/f5v90PU3IU8VAvrr2pwcHQbvXYzyDCHmrGPgyZo38DJ84YmTJxWSvjZZMPfCSHsSx5xqIH+tiojywV6/D9PDuhHECsGj7gFRfxV/WfX6QMdoeMBPyTh9HygQXja15zglfhkqC9bfEkWDHwyU/sBdOvLuzUh2lIT0+mpqw4YflfGCicz8GcBjItFhl4juM+j5FlCi2mjQKXSWE3a15+kS8ouLNs8Fy4370Ddos67+KIdRDXG28h"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
