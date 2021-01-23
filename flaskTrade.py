from flask import Flask, request
from flask_mail import Mail, Message
from config import *
import json, requests

app = Flask(__name__)

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL ="{}/v2/orders".format(BASE_URL)
POSITIONS_URL="{}/v2/positions/SPXL".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

app.config['DEBUG']= True
app.config['TESTING']=False
app.config['MAIL_SERVER']= MAIL_SERVER
app.config['MAIL_PORT']=PORT
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
#app.config['MAIL_DEBUG']=
app.config['MAIL_USERNAME']=EMAIL
app.config['MAIL_PASSWORD']=PASSWORD
app.config['MAIL_DEFAULT_SENDER']= EMAIL
app.config['MAIL_MAIL_MAX_EMAILS']=5
#app.config['MAIL_MAIL_SUPPRESS_SEND']=False
app.config['MAIL_ASCII_ATTACHMENTS']=False

mail = Mail(app)


@app.route('/')
def hello_world():

    return 'yo :)'

def space(str):
    return print('     '+str+'     ')

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    #setup
    get_account = requests.get(ACCOUNT_URL, headers=HEADERS)
    account_response = json.loads(get_account.content)
    print(account_response)
    space("account")
    acc_info = {
        "BP" : account_response['buying_power'],
        "regt_BP": account_response['regt_buying_power'],
        "day_count" : account_response['daytrade_count'],
    }
    print(acc_info)
    space("accountInfo")
    #acc_info['day_count']=4


    position_request = requests.get(POSITIONS_URL, headers=HEADERS)
    position_response = json.loads(position_request.content)
    print(position_response)
    space("position")
    position = {
        "message":  ' ',
        "qty": ' '
    }
    
    #request = app.current_request
    webhook_message = request.json
    data = {
        "side": webhook_message['buy/sell'],                    # buy or sell
        "symbol": webhook_message['ticker'],
        "qty": 1,                            
        "type": "limit",                                        # market, limit, stop, stop_limit, or trailing_stop
        "limit_price": webhook_message['close'],                # required if type is limit or stop_limit
        "time_in_force": "gtc",                                 # day, gtc, opg, cls, ioc, fok.
    }

    print(data)
    space("data")

    # print(type(acc_info["regt_BP"]))
    # print(data['limit_price'])
    
    #stops if daytrade exceeded or not enough BP
    if acc_info['day_count'] > 3:
        return 'Day trade exceeded'
    elif float(acc_info['regt_BP']) < float(data['limit_price']):
        return 'not enough BP'


    if 'message' in position_response:
        print(position_response['message'])
    else:
        position = {
            "qty": position_response['qty']
        }


    mail_message = 'MERP'
    if data['side'] == 'buy':
        buy_shares = float(acc_info["regt_BP"])//float(data['limit_price'])
        print(buy_shares)
        data['qty'] = buy_shares
        mail_message = 'Buying '+str(buy_shares)+' shares'
    elif data['side'] == 'sell':
        data['qty'] == position['qty']
        mail_message = 'Selling '+str(data['qty'])+' shares'
    print(buy_shares)



    #order request
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    response = json.loads(r.content)



    print(response)
    #print('///////',response['id'],'////////')
    msg = Message(SUBJECT, recipients=[RECIPIENT])
    msg.html = '<b>'+mail_message+'<br> Equity at '+str(account_response['equity'])+'</b>'
    mail.send(msg)
    return {
        'message': 'I bought the stock',
        'webhook_message': webhook_message
        
    }





if __name__ == '__main__':
    app.run()




