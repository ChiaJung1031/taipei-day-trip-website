from flask import *
import mysql.connector
from mysql.connector import errorcode

mydb= mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="website"
)

def getdata(page,keyword):
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




def getattractid(id):
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










