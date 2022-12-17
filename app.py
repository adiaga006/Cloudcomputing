from flask import render_template, Flask, request
import boto3
import json
account_id = "ASIAWIM27RKEFPF4NY33"
account_key = "xQq2a59gKr3NTCGgABRbKdz+DHEz3GNNQ1bbN0FU"
aws_token="FwoGZXIvYXdzEAQaDMGudP+xNznOa9bpmCLPAXpfjYJ9xh9PTzsE/yXtV/cikT1zfGJi2udt21cDmz07V893TTti2Fj5dwWFmt3i+4Rl+p/FWOPgUIHNsQLDspBlghUp2+2GgryTnWtydSKRy6xSmNCn1K4msyZh1jVNi0ljWrnLjAP8ESpV9f2dZa0BJ/2uqlMnnNfYUIXyREOqUn0Wc/+S9cPhWgfRv0DA/bI51j6JKFKm/SoEVhe2nrAFqvt3TM9bSU+8jihF8kUtUPoPKW+XORFGuLvfV2CRqJQF3TDWHIShm4djyiNsByjgwvacBjItBhYU9IY47v5TUrq0J4SofXa4SZtBj74/rj8Zs0Bwe2abQoas/8TxSJn11X5B"
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
