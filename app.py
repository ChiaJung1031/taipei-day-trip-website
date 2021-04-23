from flask import *
import mysql.connector
from mysql.connector import errorcode
mydb= mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="website"
)
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS']=False

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

@app.route("/api/attractions")
def apiattract():
	page=request.args.get("page","")
	keyword=request.args.get("keyword","")
	with mydb.cursor() as cursor:
		if keyword == None or keyword == "" and page != "":
			sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel"
			cursor.execute(sql)
			myresult = cursor.fetchall() 
			count=len(myresult)
			if  count > 12 and count != 0:
				num=count%12  #餘數
				newnum=count/12  #整數
				if num != 0:
						if int(page) < newnum +1 :
							travellist=[]
							a=int(page)*12
							for i in range(a,a+12):
								data=myresult[i]
								newimg=""
								#print(data[0])
								img=data[9].split('http')
								for j in img:
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
							All={'nextpage':int(page)+1,'data':travellist} 
							return jsonify(All)
						else:
								msg = {"error": True, "message": "查無資料"}
								return jsonify(msg)

			elif  count<= 12 and count != 0:
				travellist=[]
				for row in myresult:
					newimg=""
					img=row[9].split('http')
					for j in img:
					  newimg += "http"+j+","	
					  newimgQ=	newimg[:-1]		
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
				
				All={'nextpage':None,'data':travellist}  
				return jsonify(All)
			elif len(myresult) == 0:
				msg = {"error": True, "message": "查無資料"}
				return jsonify(msg)

		elif keyword != None or keyword != "" and page != "":
			sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel WHERE stitle LIKE '%"+keyword+"%' "
			cursor.execute(sql)
			myresult = cursor.fetchall()  
			if len(myresult) <= 12 and len(myresult) != 0:
				travellist=[]
				for row in myresult:
					newimg=""
					img=row[9].split('http')
					for j in img:
					  newimg += "http"+j+","	
					  newimgQ=	newimg[:-1]		
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
				  
				All={'nextpage':None,'data':travellist}  
				return jsonify(All)
			elif len(myresult) == 0:
				msg = {"error": True, "message": "查無資料"}
				return jsonify(msg)
			elif len(myresult) > 12:
				print(len(myresult))
				num=len(myresult)%12  #餘數
				newnum= int(len(myresult)/12) #整
				
				
				if num != 0:
						if int(page) < newnum +1 :
							travellist=[]
							print(newnum)
							a=int(page)*12
							if int(page) == newnum:
								for i in range(a,len(myresult)):
									print(myresult[i])
									data=myresult[i]
									newimg=""
									img=data[9].split('http')
									for j in img:
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
								All={'nextpage':int(page)+1,'data':travellist} 
								return jsonify(All)

							elif int(page) != newnum:
								for i in range(a,a+12):
									data=myresult[i]
									newimg=""
									img=data[9].split('http')
									for j in img:
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
								All={'nextpage':int(page)+1,'data':travellist} 
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
						for j in img:
							newimg += "http"+j+","	
							newimgQ=	newimg[:-1]		
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







app.run(port=3000)