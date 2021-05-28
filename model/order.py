import mysql.connector,requests
from mysql.connector import errorcode
from flask import *
from datetime import datetime
import json

mydb= mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="website"
)

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
        tripdatetime=orderdata["order"]["trip"]["date"]
        triptime=orderdata["order"]["trip"]["time"]
        price=orderdata["order"]["price"]
        prime=orderdata["prime"]
        paystatus = "1" #尚未付款
        bank_transaction_id="" #銀行端的訂單編號
        #訂單編號用日期+時間
        x = datetime.now()
        number=x.strftime('%Y%m%d%H%M%S%f')
        with mydb.cursor() as cursor:
                sql="INSERT INTO orders(number,name,email,phone,attId,datetime,time,price,paystatus,bank_transaction_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(number,username,email,phone,attId,tripdatetime,triptime,price,paystatus,bank_transaction_id)
                cursor.execute(sql,val)
                mydb.commit()
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
        print(pay_response,"-----------------------------------------------------------")
        if pay_response["status"] == 0:
            paystatus = "0" #付款成功
            with mydb.cursor() as cursor:
                sql="UPDATE orders SET paystatus='"+paystatus+"',bank_transaction_id='"+pay_response["bank_transaction_id"]+"' WHERE number='"+number+"'"
                cursor.execute(sql)
                mydb.commit()
                if cursor.rowcount == 1 :
                    data = {"data":{"number":number,"payment":{"status":0,"message":"付款成功"}}}
                    #付款成功-刪除預定資料
                    sql_delete="DELETE FROM booking WHERE email='"+mail+"'"
                    cursor.execute(sql_delete)
                    mydb.commit()
                    return jsonify(data)
                else:
                    return jsonify({"error":True,"message":"訂單建立失敗喔"})   
        else:
            print("回傳失敗","-----------------------------------------------------------")
            return jsonify({"error":True,"message":"訂單建立失敗，輸入不正確或其他原因"})   
    else:
        return jsonify({"error":True,"message":"未登入系統，拒絕存取"})


def getorder(num):
    mail = session.get('email')  
    name = session.get('name')
    if mail != None and name != None:
        with mydb.cursor() as cursor:
            sql="SELECT number,name,email,phone,attId,datetime,time,price FROM orders WHERE number='"+num+"'"
            cursor.execute(sql)
            myresult=cursor.fetchall()
            if len(myresult) == 1:
                for i in myresult:
                    data={
                            "data": {
                                "number":i[0],
                                "price": i[7],
                                "trip": {
                                "attraction": {
                                    "id": i[4],
                                },
                                "date": i[5],
                                "time": i[6]
                                },
                                "contact": {
                                "name": i[1],
                                "email": i[2],
                                "phone": i[3]
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






   
