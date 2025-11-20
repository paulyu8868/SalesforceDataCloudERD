import requests
import os
from utils import getSettings
from dotenv import load_dotenv

load_dotenv() # .env에서 환경변수 가져오기

def getOauthToken():
    # .env에서 계정정보 불러오기
    client_id = os.getenv('SF_CLIENT_ID')
    client_secret = os.getenv('SF_CLIENT_SECRET')
    username = os.getenv('SF_USERNAME')
    password = os.getenv('SF_PASSWORD')
    login_url = getSettings()
    login_url = login_url['login_url']
    token_url = f"{login_url}/services/oauth2/token"
    
    # payload에 요청 정보 저장
    payload = {
        'grant_type': 'password', # Username-Password Flow
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password
    }
    try:
        response = requests.post(token_url, data=payload)
        return response.json()
    except Exception as e:
        print(f'토큰 발급 오류: {e}')
        return  

if __name__ == '__main__': # 토큰 발급 테스트
    # 토큰 발급
    oauth = getOauthToken()
    access_token = oauth['access_token']
    instance_url = oauth['instance_url']
    print(access_token)
    print(instance_url)