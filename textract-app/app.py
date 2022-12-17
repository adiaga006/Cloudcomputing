from flask import render_template, Flask, request
import boto3
import json
account_id = "ASIAWIM27RKEERO4UDEY"
account_key = "NaaQ97WMYDRQgZW6RM43OwJt7PW/vrokgwlSaOoP"
aws_token="FwoGZXIvYXdzEAMaDG2Q0JlTsqOPrMLXjyLPAUKrEIr1SBag3qBxgE37mmxjOqUPWixcG3hBGmWhHY4cbXLEcqafqonYg9F0Eb4O2rFN/mtG1wcpp7GA2/BivOx6XJdRpuKi9elnEdLcLQqwvl8q7ci0FNyRyOW2Ahuywb+Rsna/dLc56FVc0sGjnUXzDYw9+4Rs3GdQJaZi+U7XBgK1jEArzGhxmgU43QzLqgnndMBjEOl7qpwwezHwu94TfJxz65z1W4ViCRJ/Axy/Bv6Iq08kFGZeNxucddKSlTOMkryKxVMp+rOfXpm/Rij0lPacBjIt36Ap8thX1kP1YEOsrSKzmVGnxJi5MMoUPsMj7O/ez8mth4WmojxOmqt1Nx19"
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
