from flask import *
import mysql.connector
from mysql.connector import errorcode
from datetime import timedelta
mydb= mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="website"
)


app=Flask(__name__, static_url_path="/", static_folder="image")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS']=False
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=30)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions",methods=['GET', 'POST'])
def apiattract():
	page=request.args.get("page","0")
	keyword=request.args.get("keyword","")
	x=int(page)*12
	limitnum= str(x)
	if keyword == None or keyword == "" and page != "":	
		with mydb.cursor() as cursor:
			sqlcount="SELECT count(*) FROM travel"
			cursor.execute(sqlcount)
			resultCount = cursor.fetchall()
			for a in resultCount:
				allcount = a[0]  # 資料總數
			num=allcount%12  #餘數
			newnum=int(allcount/12)  #整數
			sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.travel LIMIT "+limitnum+",12 "
			cursor.execute(sql)
			myresult = cursor.fetchall() 
			travellist=[]
			count=len(myresult)
			if count != 0:
							for i in range(0,count):
								data=myresult[i]
								newimg=""
								img=data[9].split('http')
								for j in img[1:len(img)]:
									newimg += "http"+j+","	
									newimgQ=newimg[:-1]		
								newitem={}
								newitem['id'] = int(data[0])
								newitem['name'] = data[1]	
								newitem['category'] = data[2]
								newitem['description'] = data[3]
								newitem['address'] = data[4] 
								newitem['transport'] = data[5]
								newitem['mrt'] = data[6]
								newitem['latitude'] = data[7]
								newitem['longtitude'] = data[8]
								newitem['images'] = [newimgQ]
								travellist.append(newitem)
							if int(page) <= newnum :
								if num == 0: #沒有餘數:下一頁
									All={'nextpage':None,'data':travellist} 
									return jsonify(All)
								else:
									if int(page) == newnum:
										All={'nextpage':None,'data':travellist} 
										return jsonify(All)
									else:
										All={'nextpage':int(page)+1,'data':travellist}
										return jsonify(All)
										
							elif int(page) > newnum:
								All={'nextpage':None,'data':travellist} 
								return jsonify(All)
							
			else:
				msg = {"error": True, "message": "查無資料"}
				return jsonify(msg)

	elif keyword != None or keyword != "" and page != "":
		with mydb.cursor() as cursor:
			sqlcount="SELECT count(*) FROM travel WHERE stitle LIKE '%"+keyword+"%' "
			cursor.execute(sqlcount)
			resultCount = cursor.fetchall()
			for a in resultCount:
				allcount = a[0]  # 資料總數
			num=allcount%12  #餘數
			newnum=int(allcount/12)  #整數
			sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel WHERE stitle LIKE '%"+keyword+"%' LIMIT "+limitnum+",12  "
			cursor.execute(sql)
			myresult = cursor.fetchall()  
			travellist=[]
			count=len(myresult)
			if count != 0:
							for i in range(0,count):
								data=myresult[i]
								newimg=""
								img=data[9].split('http')
								for j in img[1:len(img)]:
									newimg += "http"+j+","	
									newimgQ=newimg[:-1]		
								newitem={}
								newitem['id'] = int(data[0])
								newitem['name'] = data[1]	
								newitem['category'] = data[2]
								newitem['description'] = data[3]
								newitem['address'] = data[4] 
								newitem['transport'] = data[5]
								newitem['mrt'] = data[6]
								newitem['latitude'] = data[7]
								newitem['longtitude'] = data[8]
								newitem['images'] = [newimgQ]
								travellist.append(newitem)
							if int(page) <= newnum :
								if num == 0: #沒有下一頁
									All={'nextpage':None,'data':travellist} 
									return jsonify(All)
								else:
									if int(page) == newnum:
										All={'nextpage':None,'data':travellist} 
										return jsonify(All)
									else:
										All={'nextpage':int(page)+1,'data':travellist}
										return jsonify(All)
										
							elif int(page) > newnum:
								All={'nextpage':None,'data':travellist} 
								return jsonify(All)
							
	else:
		msg = {"error": True, "message": "查無資料"}
		return jsonify(msg)


@app.route("/api/attraction/<attractionId>",methods=["GET"])
def apiattractid(attractionId):
	id=attractionId
	with mydb.cursor() as cursor:
		if id.isdigit():
				sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel WHERE id= "+id+""
				cursor.execute(sql)
				myresult = cursor.fetchall()  
				travellist=[]
				if len(myresult) == 0:
					msg = {"error": True, "message": "景點編號不正確"}
					return jsonify(msg)
				else:
					for row in myresult:
						newimg=""
						img=row[9].split('http')
						for j in img[1:len(img)]:
							newimg += "http"+j+","	
							newimgQ=newimg[:-1]		
						newitem={}
						newitem['id'] = int(row[0])
						newitem['name'] = row[1]	
						newitem['category'] = row[2]
						newitem['description'] = row[3]
						newitem['address'] = row[4] 
						newitem['transport'] = row[5]
						newitem['mrt'] = row[6]
						newitem['latitude'] = row[7]
						newitem['longtitude'] = row[8]
						newitem['images'] = [newimgQ]
						travellist.append(newitem)
					All={'data':travellist}  
					return jsonify(All)
		else:
			msg = {"error": True, "message": "編號輸入錯誤"}
			return jsonify(msg)


@app.route("/api/user",methods=["POST"])
def apiusersignup():
	password=request.args.get("password","")
	email=request.args.get("email","")
	username=request.args.get("name","")
	if request.method == "POST":
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

@app.route("/api/user",methods=["PATCH"])
def apiusersignin():
	password=request.args.get("password","")
	email=request.args.get("email","")
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

@app.route("/api/user",methods=["GET"])
def apiusercheck():
	if request.method == "GET":
		id = session.get('id') 
		email = session.get('email')  
		name = session.get('name') 
		print(id,"...............................................................................")
		if id != None and email != None and name != None :
			data = {"data":{"id":id,"name":name,"email":email}}
			return jsonify(data)
		else:
			data = {"data":None}
			return jsonify(data)

@app.route("/api/user",methods=["DELETE"])
def apiuserlogout():
	session.clear()
	data = {"ok":True}
	return jsonify(data)
			


@app.route("/api/booking",methods=["POST"])
def newbooking():
	postdata = request.json
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
		print(result,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
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


@app.route("/api/booking",methods=["GET"])
def getbooking():
	mail = session.get('email')  
	name = session.get('name')
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

@app.route("/api/booking",methods=["DELETE"])
def deletebooking():
	mail = session.get('email') 
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




app.run(host="0.0.0.0",port=3000)