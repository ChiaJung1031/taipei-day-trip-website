from flask import *
from sql_database import select_att_id,select_count,select_attraction


def getdata(page,keyword):
	x=int(page)*12
	limitnum= str(x)
	if keyword == None or keyword == "" and page != "":	
			count_data = select_count(kw="nokeyword")
			for a in count_data:
				allcount = a  # 資料總數
			num=allcount%12  #餘數
			newnum=int(allcount/12)  #整數
			select_att_data = select_attraction(limitnum)
			travellist=[]
			count=len(select_att_data)
			if count != 0:
							for i in range(0,count):
								data=select_att_data[i]
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
			count_data = select_count(kw=keyword)
		#with mydb.cursor() as cursor:
			#sqlcount="SELECT count(*) FROM travel WHERE stitle LIKE '%"+keyword+"%' "
			#cursor.execute(sqlcount)
			#resultCount = cursor.fetchall()
			for a in count_data:
				allcount = a  # 資料總數
			num=allcount%12  #餘數
			newnum=int(allcount/12)  #整數
			
			select_att_data = select_attraction(keyword,limitnum)
			#sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel WHERE stitle LIKE '%"+keyword+"%' LIMIT "+limitnum+",12  "
			#cursor.execute(sql)
			#myresult = cursor.fetchall()  
			travellist=[]
			count=len(select_att_data)
			if count != 0:
							for i in range(0,count):
								data=select_att_data[i]
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
    #with mydb.cursor() as cursor:
        if id.isdigit():
            select_data = select_att_id(id)
            #sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel WHERE id= "+id+""
            #cursor.execute(sql)
           # myresult = cursor.fetchall()
            travellist=[]
            if select_data == None:
                msg = {"error": True, "message": "景點編號不正確"}
                return jsonify(msg)
            else:
                for row in select_data:
                    newimg=""
                    img=select_data["file"].split('http')
                    for j in img[1:len(img)]:
                        newimg += "http"+j+","	
                    newimgQ=newimg[:-1]	
                    newitem={}
                    newitem['id'] = select_data["id"]
                    newitem['name'] = select_data["stitle"]	
                    newitem['category'] = select_data["CAT2"]
                    newitem['description'] = select_data["xbody"]
                    newitem['address'] = select_data["address"] 
                    newitem['transport'] = select_data["info"]
                    newitem['mrt'] = select_data["MRT"]
                    newitem['latitude'] = select_data["latitude"]
                    newitem['longtitude'] = select_data["longitude"]
                    newitem['images'] = newimgQ
                    travellist.append(newitem)
                    All={'data':travellist}  
                    return jsonify(All)
        else:
            msg = {"error": True, "message": "編號輸入錯誤"}
            return jsonify(msg)










