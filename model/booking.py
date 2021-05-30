from flask import *
import mysql.connector
from mysql.connector import errorcode

mydb= mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="website"
)

def newbook(postdata):
	attractionId =postdata["attractionId"]
	date = postdata["date"]
	time = postdata["time"]
	price = postdata["price"]
	mail = session.get('email')  
	name = session.get('name')
	with mydb.cursor() as cursor:
		sql_select = "SELECT * FROM booking WHERE email = '"+mail+"'"
		cursor.execute(sql_select)
		result=cursor.fetchall()
		if mail != None and name != None:
			if len(result) == 1:
				sql = "UPDATE booking SET attractionId='"+attractionId+"',date='"+date+"',time='"+time+"',price='"+price+"' WHERE email='"+mail+"'"
				cursor.execute(sql)
				mydb.commit()
				if cursor.rowcount == 1:
					result = {"ok":True}
					return jsonify(result)
				else:
					result = {"error":True,"message":"建立更新失敗，輸入不正確"}
					return jsonify(result)			
			else:
				sql = "INSERT INTO booking (email,attractionId,date,time,price) VALUES (%s,%s,%s,%s,%s)"
				val = (mail,attractionId,date,time,price)
				cursor.execute(sql,val)
				mydb.commit()
				if cursor.rowcount == 1:
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
            sql_book ="SELECT attractionid,date,time,price FROM booking WHERE email='"+mail+"'"
            with mydb.cursor() as cursor:
                cursor.execute(sql_book)
                result=cursor.fetchall()
                if len(result) !=0:
                    for i in result:
                        attractId=str(i[0])
                        date=i[1]
                        time=i[2]
                        price=i[3]
                    sql_attract="SELECT id,stitle,address,file FROM travel WHERE id='"+attractId+"'"
                    cursor.execute(sql_attract)
                    result_2=cursor.fetchall()
                    for n in result_2:
                        id=n[0]
                        name=n[1]
                        address=n[2]
                        image=n[3].split('http')[1]
                    data={"data":{"attraction":{"id":id,"name":name,"address":address,"image":"http"+image},"date":date,"time":time,"price":price}}
                    return jsonify(data)
                else:
                    data={"data":None}
                    return jsonify(data)
        else:
            data={"error":True,"message":"未登入系統，拒絕存取"}
            return jsonify(data)

def deletebook(mail):
        with mydb.cursor() as cursor:
            sql="DELETE FROM booking WHERE email='"+mail+"'"
            cursor.execute(sql)
            mydb.commit()
            if cursor.rowcount == 1:
                result = {"ok":True}
                return jsonify(result)
            else:
                result = {"error":True,"message":"未登入系統，拒絕存取"}
                return jsonify(result)

