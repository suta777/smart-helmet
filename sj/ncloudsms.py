import hashlib
import hmac
import base64
import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

def sendmsg(to_number="01089475740", content="메세지 내용이야"):

    # 메세지 정보
    from_number = "01089475740"
    sms_type = "SMS"  # 메세지 종류 SMS, LMS, MMS
    content_type = "COMM"  # 메시지 타입, COMM: 일반, AD: 광고
    country_number = "82"  # 국가 코드, 디폴트: 82

    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # Ncloud API Key 설정
    ncloud_accesskey = os.environ.get("ncloud_accesskey")
    ncloud_secretkey = os.environ.get("ncloud_secretkey")
    serviceId = os.environ.get("serviceId")

    # 암호화 문자열 생성을 위한 기본값 설정
    apicall_method = "POST"
    space = " "
    new_line = "\n"

    # API 서버 정보
    api_url = "https://sens.apigw.ntruss.com"

    # API URL
    api_uri = f"/sms/v2/services/{serviceId}/messages"

    # hmac으로 암호화할 문자열 생성
    hmac_message = apicall_method + space + api_uri + \
        new_line + timestamp + new_line + ncloud_accesskey
    hmac_message = bytes(hmac_message, 'UTF-8')

    # hmac_sha256 암호화
    ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
    signingKey = base64.b64encode(
        hmac.new(ncloud_secretkey, hmac_message, digestmod=hashlib.sha256).digest())

    # http 호출 헤더값 설정
    http_header = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": ncloud_accesskey,
        "x-ncp-apigw-signature-v2": signingKey
    }

    # POST 파라미터
    request_data = {
        "type": sms_type,
        "contentType": content_type,
        "countryCode": country_number,
        "from": from_number,
        "content": content,
        "messages": [
            {
                "to": to_number,
                "content": content
            }
        ]
    }

    # api 호출
    response = requests.post(api_url + api_uri,
                             headers=http_header, data=json.dumps(request_data))
    return response.text
