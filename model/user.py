import mysql.connector
from mysql.connector import errorcode
from flask import *
from sql_database import select_user,insert_user


def signup(password,email,username):
	#with mydb.cursor() as cursor:
		if email !="" and username !="" and password !="":
				select_data = select_user(user_email=email)		
				#sql="SELECT email,name,id FROM user WHERE email= '"+email+"'"
				#cursor.execute(sql)
				#result = cursor.fetchone()
				#orderData = dict(zip(cursor.column_names, result))
				if select_data == "sameEmail":
					data = {"error":True,"message":"註冊失敗，請確認Email是否重複"}
					return jsonify(data)
				else:
					insert_data = insert_user(email=email,name=username,psw=password)
					#sql = "INSERT INTO user (name,email,password) VALUES (%s,%s,%s)"
					#value = (username,email,password)
					#cursor.execute(sql,value)
					#mydb.commit()
					#print(cursor.rowcount, "record(s) affected")
					if insert_data == "insertDone" :
						data = {"ok":True}
						return jsonify(data)
					else:
						data = {"error":True,"message":"註冊失敗，請確認Email是否重複"}
						return jsonify(data)


def signin(password,email):
	#with mydb.cursor() as cursor:
		if password !="" and email !="":
				select_data = select_user(user_email=email,psw=password)	
				#sql = "SELECT id,email,name FROM user WHERE email=%s AND password=%s"
				#value = (email,password)
				#cursor.execute(sql,value)
				#myresult = cursor.fetchall()
				if select_data != None:
					for i in select_data:
						session["id"]=select_data["id"]
						session["email"]=select_data["email"]
						session["name"]=select_data["name"]
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