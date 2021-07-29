import requests
import payconfiguration
import json
from datetime import datetime

def get_api_token():
    url = "http://34.81.78.27/PayPayDrinkBackend/api/auth/login"

    payload = "{\r\n    \"account\":\"api\",\r\n    \"password\":\".iaKVMVf_8h_1i9y\"\r\n}"
    headers = { 'Content-Type': 'application/json' }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    responseJson = json.loads(response.text)
    payconfiguration.API_TOKEN = responseJson['access_token']  
    
def checkToken():

    url = f"http://34.81.78.27/PayPayDrinkBackend/api/auth/me?token={payconfiguration.API_TOKEN}"
    print(url)
    payload={}
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)
    return response.status_code
def report_cup_num(cup_num):
    url = f"http://34.81.78.27/PayPayDrinkBackend/api/reportCup?token={payconfiguration.API_TOKEN}"
    print(url)
    today=datetime.now()
    todayStr=today.strftime('%Y-%m-%d %H:%M:%S')
    # print(todayStr)
    # payload = f"{\r\n    \"ip\":\"211.22.7.186\", /* 樹苺派IP */\r\n    \"date\":\"{todayStr}\", /* 做完的日期時間 */\r\n    \"cupnum\":\"{cup_num}\" /* 當初傳過去的cupnum */\r\n}"
    # payload = "{ 'ip':'211.22.7.186','date':'todayStr}','cpunum':'cup_num'}'}"
    payload={"ip": '211.22.7.186', "date": todayStr,"cupnum":cup_num}
    print("----")

    print(json.dumps(payload))
    

    headers = { 'Content-Type': 'application/json' }
   
    
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
def sendAPItoken(cup_num):
    get_api_token()
    if (checkToken()==200):
       report_cup_num(cup_num)
    else :
        print('error server api')
        
# sendAPItoken('a1234')
# def main():    
#    sendAPItoken()
#     # report_cup_num("1.2.3.4",'A1234')
    
    

# main()
