import json
import mysql.connector
from mysql.connector import errorcode
mydb= mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="website"
)

#cursor=mydb.cursor()
with open("taipei-attractions.json", mode="r",encoding="utf-8") as file:
 data=json.load(file)
 all=data["result"]["results"]
 for news in all:
          idnum=news["_id"]  #id
          print(idnum)
          info=news["info"]   #info
          stitle= news["stitle"] #stitle
          xpostDate= news["xpostDate"] #xpostDate
          longitude= news["longitude"] #longitude
          REF_WP= news["REF_WP"] #REF_WP
          avBegin= news["avBegin"] #avBegin
          MRT= news["MRT"] #MRT
          langinfo= news["langinfo"] #langinfo
          SERIAL_NO= news["SERIAL_NO"] #SERIAL_NO
          RowNumber= news["RowNumber"] #RowNumber
          CAT1= news["CAT1"] #CAT1
          CAT2= news["CAT2"] #CAT2
          MEMO_TIME= news["MEMO_TIME"] #MEMO_TIME
          POI= news["POI"] #POI
          idpt= news["idpt"] #idpt
          latitude= news["latitude"] #latitude
          xbody= news["xbody"] #xbody
          avEnd= news["avEnd"] #avEnd
          address= news["address"] #address
          files= news["file"].split("http") #file
          filestring =""
          for j in files:
           newfilename=j[-3:] 
           if newfilename=="jpg" or newfilename=="JPG" or newfilename=="png" or newfilename=="PNG":
                filestring += "http"+ j  
          with mydb.cursor() as cursor:
           sql = "INSERT INTO travel(id,info,stitle,xpostDate,longitude,REF_WP,avBegin,langinfo,MRT,SERIAL_NO,RowNumber,CAT1,CAT2,MEMO_TIME,POI,file,idpt,latitude,xbody,avEnd,address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
           val = (idnum,info,stitle,xpostDate,longitude,REF_WP,avBegin,langinfo,MRT,SERIAL_NO,RowNumber,CAT1,CAT2,MEMO_TIME,POI,filestring,idpt,latitude,xbody,avEnd,address)
           cursor.execute(sql,val)
           mydb.commit()  
      


        
            
       
