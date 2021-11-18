import requests
import payconfiguration
import json
from datetime import datetime
import time
def get_api_token():
    print('get_token')
    url = "https://paypaydrink.com/PayPayDrinkBackend/api/auth/login"

    payload = "{\r\n    \"account\":\"api\",\r\n    \"password\":\".iaKVMVf_8h_1i9y\"\r\n}"
    headers = { 'Content-Type': 'application/json' }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    responseJson = json.loads(response.text)
    payconfiguration.API_TOKEN = responseJson['access_token']  
    
def checkToken():

    url = f"https://paypaydrink.com/PayPayDrinkBackend/api/auth/me?token={payconfiguration.API_TOKEN}"
    print(url)
    payload={}
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)
    return response.status_code
def report_cup_num(cup_num):
    url = f"https://paypaydrink.com/PayPayDrinkBackend/api/reportCup?token={payconfiguration.API_TOKEN}"
    print(url)
    today=datetime.now()
    todayStr=today.strftime('%Y-%m-%d %H:%M:%S')
    # print(todayStr)
    # payload = f"{\r\n    \"ip\":\"211.22.7.186\",    \"date\":\"{todayStr}\",    \"cupnum\":\"{cup_num}\" }"
    # payload = "{ 'ip':'211.22.7.186','date':'todayStr}','cpunum':'cup_num'}'}"
    # payload = "{\r\n    \"ip\":\"192.168.1.1\", \r\n    \"date\":\"2021-07-21 01:22:22\",  */\r\n    \"cupnum\":\"z9999\"\r\n}"
    payload={"ip": '211.22.7.186', "date": todayStr,"cupnum":cup_num}
    # payload="{'ip': '211.22.7.186','date': '2021-07-28 11:10:00','cupnum':'Z9999'}"
    # payload=payload.replace("'","\"")
    # payloadok=f"{'ip': '211.22.7.186','date': '{todayStr}','cupnum':'{cup_num}'}"
    # payloadok=payloadok.replace("'","\"")
    print("----")

    jsondata=json.dumps(payload)
    print(jsondata)

    headers = { 'Content-Type': 'application/json' }
   
    
    response = requests.request("POST", url, headers=headers, data=jsondata)

    print(response.text)
def report_num2(cup_num):

    url = f"https://paypaydrink.com/PayPayDrinkBackend/api/reportCup?token={payconfiguration.API_TOKEN}"

    # payload="{\r\n    \"ip\": \"211.22.7.186\",\r\n    \"date\": \"2021-07-28 11:10:00\",\r\n    \"cupnum\": \"Z9999\"\r\n}"
    payload="{'ip': '211.22.7.186','date': '2021-07-28 11:10:00','cupnum':'Z9999'}"
    payload=payload.replace("'","\"")
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def sendAPItoken(cup_num):

    if (checkToken()==200):
        report_cup_num(cup_num)
        # report_num2('Z9999')
        # report_cup_num(cup_num)
    else :
        get_api_token()
        if (checkToken()==200):
            report_cup_num(cup_num)
        else:
            print('error server api')
        
# sendAPItoken('a1234')

def main():    
   sendAPItoken('Z9999')
   time.sleep(1)
   sendAPItoken('Z9998')
   sendAPItoken('Z9997')
    # report_cup_num("1.2.3.4",'A1234')

# main()

if __name__ == "__main__":
    main()
