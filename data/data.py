import json
from sql_database import insert_travel_data



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
          sql_insertdata = insert_travel_data(id=idnum,info=info,stitle=stitle,xpostDate=xpostDate,longitude=longitude,REF_WP=REF_WP,avBegin=avBegin,langinfo=langinfo,MRT=MRT,SERIAL_NO=SERIAL_NO,RowNumber=RowNumber,CAT1=CAT1,CAT2=CAT2,MEMO_TIME=MEMO_TIME,POI=POI,file=filestring,idpt=idpt,latitude=latitude,xbody=xbody,avEnd=avEnd,address=address)



        
            
       
