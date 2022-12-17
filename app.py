from flask import render_template, Flask, request
import boto3
import json
account_id = "ASIAUDCPFZHIUBP6G2OF"
account_key = "8PWLxbQVPDVHgMt+YEjqv0wDwUTLC1gkvils+b5p"
aws_token="FwoGZXIvYXdzEAUaDFTd0zkxysN4xh/YCiLPAZ1hus4DTLL10fyocFaXnGGhdgTq/thhn+/R81glpy3kvptYJQhhpfByiiSZ97u+cM78ANiwBKvk2F+g4zwd+dfR+nlp1jHnud0T9/NLrCCf0tJGCF1oKQyWzcPubZfpJYSxOmit7OTgYt9bJgVwQR5tP9H7yzy3uI1WawAUApe8quKFYcRe0gNogYj2fqQr0QhfmZzYrbADWM+mdWTvlAUusHLr5gJJgg8kO7MF5y3bXC850kwgrozdNiFz1WemuKxYSlWkUkMwZioeI+KFGSjU3PacBjItEXMheU8voQ/OJ+YsTc7faMlX5UH6evCObq42+GD/hucap1I92WXzmvdOz1g3"
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
