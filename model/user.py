import mysql.connector
from mysql.connector import errorcode
from flask import *

mydb= mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="website"
)

def signup(password,email,username):
	with mydb.cursor() as cursor:
		if email !="" and username !="" and password !="":
				sql="SELECT email FROM user WHERE email= '"+email+"'"
				cursor.execute(sql)
				result = cursor.fetchall()
				if len(result) == 1:
					data = {"error":True,"message":"註冊失敗，請確認Email是否重複"}
					return jsonify(data)
				else:
					sql = "INSERT INTO user (name,email,password) VALUES (%s,%s,%s)"
					value = (username,email,password)
					cursor.execute(sql,value)
					mydb.commit()
					print(cursor.rowcount, "record(s) affected")
					if cursor.rowcount == 1 :
						data = {"ok":True}
						return jsonify(data)
					else:
						data = {"error":True,"message":"註冊失敗，請確認Email是否重複"}
						return jsonify(data)


def signin(password,email):
	with mydb.cursor() as cursor:
		if password !="" and email !="":
				sql = "SELECT id,email,name FROM user WHERE email=%s AND password=%s"
				value = (email,password)
				cursor.execute(sql,value)
				myresult = cursor.fetchall()
				if len(myresult) == 1 :
					for i in myresult:
						session["id"]=i[0]
						session["email"]=i[1]
						session["name"]=i[2]
						data = {"ok":True}
						return jsonify(data)
				else:
					session["email"]= False
					session["password"]= False
					data = {"error":True,"message":"登入失敗，帳號或密碼錯誤"}
					return jsonify(data)


def checkuser(id,email,name):
    if id != None and email != None and name != None :
        data = {"data":{"id":id,"name":name,"email":email}}
        return jsonify(data)
    else:
        data = {"data":None}
        return jsonify(data)

def deleteuser():
    session.clear()
    data = {"ok":True}
    return jsonify(data)