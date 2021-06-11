from flask import *
from datetime import datetime
import json,requests
from model.booking import deletebook
from sql_database import insert_order,update_order,select_order

def neworder(orderdata):
    mail = session.get('email')  
    name = session.get('name')
    if mail != None and name != None:
        username=orderdata["order"]["contact"]["name"]
        email=orderdata["order"]["contact"]["email"]
        phone=orderdata["order"]["contact"]["phone"]
        attId=orderdata["order"]["trip"]["attraction"]["id"]
        attName=orderdata["order"]["trip"]["attraction"]["name"]
        attAddress=orderdata["order"]["trip"]["attraction"]["address"]
        attImage=orderdata["order"]["trip"]["attraction"]["image"]
        tripdate=orderdata["order"]["trip"]["date"]
        triptime=orderdata["order"]["trip"]["time"]
        price=orderdata["order"]["price"]
        prime=orderdata["prime"]
        paystatus = "1" #尚未付款
        bank_transaction_id="" #銀行端的訂單編號
        #訂單編號用日期+時間
        x = datetime.now()
        number=x.strftime('%Y%m%d%H%M%S%f')
        inser_data = insert_order(username=username,email=email,phone=phone,attId=attId,tripdate=tripdate,triptime=triptime,price=price,paystatus=paystatus,number=number,bank_transaction_id=bank_transaction_id)
        if inser_data == "insertDone":
            ####金流交易#####      
            url_pay="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
            header_pay={ "Content-Type": "application/json","x-api-key":"partner_nDaEB0LzhKmrbWduC3fuLS4lHbLaUub6eVfmfp27QjjFdpfABILgqebc"}
            data_pay=json.dumps({
                        "prime": prime,
                        "partner_key": "partner_nDaEB0LzhKmrbWduC3fuLS4lHbLaUub6eVfmfp27QjjFdpfABILgqebc",
                        "merchant_id": "leeapun_ESUN",
                        "details":"TapPay Test",
                        "amount": price,
                        "cardholder": {
                            "phone_number": phone,
                            "name": username,
                            "email":email,
                            "zip_code": "",
                            "address": "",
                            "national_id": ""
                        }
                    })  

            response = requests.post(url_pay, data = data_pay, headers = header_pay, timeout = 30)
            pay_response=response.json()
            if pay_response["status"] == 0:
                paystatus = "0" #付款成功
                update_data = update_order(paystatus=paystatus,bank_transaction_id=pay_response["bank_transaction_id"],number=number)
                if update_data == "updateDone" :
                    data = {"data":{"number":number,"payment":{"status":0,"message":"付款成功"}}}
                    #付款成功-刪除預定資料
                    deletebook(mail)
                    return jsonify(data)
                else:
                    return jsonify({"error":True,"message":"訂單建立失敗喔"})   
            else:
                return jsonify({"error":True,"message":"訂單建立失敗，輸入不正確或其他原因"})   
    else:
        return jsonify({"error":True,"message":"未登入系統，拒絕存取"})


def getorder(num):
    mail = session.get('email')  
    name = session.get('name')
    if mail != None and name != None:
        select_order_data = select_order(num)  
        if select_order_data != None:
            data={
                    "data": {
                        "number":select_order_data["number"],
                        "price": select_order_data["price"],
                        "trip": {
                        "attraction": {
                            "id": select_order_data["attId"],
                        },
                        "date": select_order_data["datetime"],
                        "time": select_order_data["time"]
                        },
                        "contact": {
                        "name": name,
                        "email": mail,
                        "phone": select_order_data["phone"]
                        },
                         "status": 0
                    }
                }
            return jsonify(data)
        else:
            data = {"data":None}
    else:
        data = {"error":True,"message":"未登入系統，拒絕存取"}
        return jsonify(data)






   
