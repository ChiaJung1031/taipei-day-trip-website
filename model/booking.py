from flask import *
from sql_database import delete_booking,select_booking,update_booking,insert_booking,select_att_id



def newbook(postdata):
    attractionId =postdata["attractionId"]
    date = postdata["date"]
    time = postdata["time"]
    price = postdata["price"]
    mail = session.get('email')  
    name = session.get('name')
    if mail != None and name != None:
        select_booking_data = select_booking(mail)
        if select_booking_data != None:
            update_booking_data = update_booking(attractionId=attractionId,date=date,time=time,price=price,email=mail)
            if update_booking_data == "updateDone":
                result = {"ok":True}
                return jsonify(result)
            else:
                result = {"error":True,"message":"建立更新失敗，輸入不正確"}
                return jsonify(result)			
        else:
            insert_booking_data = insert_booking(attractionId=attractionId,date=date,time=time,price=price,email=mail)
            if insert_booking_data == "insertDone":
                result = {"ok":True}
                return jsonify(result)
            else:
                result = {"error":True,"message":"建立新增失敗，輸入不正確"}
                return jsonify(result)
    else:
        result = {"error":True,"message":"未登入系統，拒絕存取"}
        return jsonify(result)


def getbook(mail,name):
        if mail != None and name != None:
            select_booking_data = select_booking(mail)
            if select_booking_data != None:
                attractId= select_booking_data["attractionId"]
                date=select_booking_data["date"]
                time=select_booking_data["time"]
                price=select_booking_data["price"]

                select_attId_data = select_att_id(str(attractId))
                if select_attId_data != None:
                    id = select_attId_data["id"]
                    name = select_attId_data["stitle"]
                    address = select_attId_data["address"]
                    image=select_attId_data["file"].split('http')[1]
                    data={"data":{"attraction":{"id":id,"name":name,"address":address,"image":"http"+image},"date":date,"time":time,"price":price}}
                    return jsonify(data)

                else:
                    data={"data":None}
                    return jsonify(data)
               
            else:
                data={"data":None}
                return jsonify(data)
        else:
            data={"error":True,"message":"未登入系統，拒絕存取"}
            return jsonify(data)

def deletebook(mail):
    delete_data = delete_booking(mail)
    if delete_data == "deleteDone":
        result = {"ok":True}
        return jsonify(result)
    else:
        result = {"error":True,"message":"未登入系統，拒絕存取"}
        return jsonify(result)




