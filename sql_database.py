from mysql.connector import pooling
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

try:
   conn_pool = pooling.MySQLConnectionPool(
      pool_name = "my_pool",
      pool_size = 5,
      pool_reset_session = True,
      host=os.getenv("DBHOST"),
      user=os.getenv("DBUSER"),
      password=os.getenv("DBPASSWORD"),
      database=os.getenv("DBDATABASE"),
      port=os.getenv("PORT"),
      charset = "utf8"
      )
except Exception as e:
   print(e)


def closePool(my_connection,my_cursor):
   my_connection.close()
   my_cursor.close()


### User ###
def select_user(**kwargs):
      try:
         if len(kwargs) == 1 :
            sql="SELECT email FROM user WHERE email= '"+kwargs["user_email"]+"'"
         if len(kwargs) == 2:
            sql="SELECT * FROM user WHERE email= '"+kwargs["user_email"]+"' AND password='"+kwargs["psw"]+"'"
         conn = conn_pool.get_connection()
         if conn.is_connected():
            newCursor = conn.cursor()
            newCursor.execute(sql)   
            myResult = newCursor.fetchone()
            if myResult != None: #有重複的帳號
               if len(kwargs) == 1:
                  data="sameEmail"
                  return data
               if len(kwargs) == 2:
                  data=dict(zip(newCursor.column_names,myResult))
                  return data
            else:
               return None
      except Exception as e:
         print(e)
         return None
      finally:
         closePool(conn, newCursor)

def insert_user(**kwargs):
   try:
         sql = "INSERT INTO user (name,email,password) VALUES (%s,%s,%s)"
         val = (kwargs["name"],kwargs["email"],kwargs["psw"])
         conn = conn_pool.get_connection()
         if conn.is_connected():
            newCursor = conn.cursor()
            newCursor.execute(sql,val)
            conn.commit()
            if newCursor.rowcount == 1 :
               return "insertDone"
            else:
               return "insertError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

### Attraction ###
def select_att_id(idnum):
   try:
      sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel WHERE id= "+idnum+""
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql)
      myResult = newCursor.fetchone()
      if myResult != None:
         data = dict(zip(newCursor.column_names,myResult))
         return data 
  
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def select_count(**kwargs):
   try:
      if kwargs["kw"] != "nokeyword":
         sqlcount="SELECT count(*) FROM travel WHERE stitle LIKE '%"+kwargs["kw"]+"%' "
      else:
         sqlcount="SELECT count(*) FROM travel"
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sqlcount)
      myResult = newCursor.fetchone()
      return myResult
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def select_attraction(*args):
   try:
      if len(args) == 1:
         for arg in args:
            limitnum = arg
         sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.travel LIMIT "+limitnum+",12 "
      if len(args) == 2:
         allarg=""
         for arg in args:
            allarg += arg + ","
         keyword = allarg.split(",")[0]
         limitnum = allarg.split(",")[1]
         sql="SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM travel WHERE stitle LIKE '%"+keyword+"%' LIMIT "+limitnum+",12  "
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql)
      myResult = newCursor.fetchall()
      return myResult
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

### Booking ###
def select_booking(email):
   try:
      sql_select = "SELECT * FROM booking WHERE email = '"+email+"'"
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql_select)
      myResult = newCursor.fetchone()
      if myResult != None:
         data = dict(zip(newCursor.column_names,myResult))
         return data
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def update_booking(**kwargs):
   try:
      attractionId = kwargs["attractionId"]
      date = kwargs["date"]
      time = kwargs["time"]
      price = kwargs["price"]
      email = kwargs["email"]
      sql = "UPDATE booking SET attractionId='"+attractionId+"',date='"+date+"',time='"+time+"',price='"+price+"' WHERE email='"+email+"'"
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql)
      conn.commit()
      if newCursor.rowcount == 1 :
         return "updateDone"
      else:
         return "updateError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def insert_booking(**kwargs):
   try:
      attractionId = kwargs["attractionId"]
      date = kwargs["date"]
      time = kwargs["time"]
      price = kwargs["price"]
      email = kwargs["email"]
      sql = "INSERT INTO booking (email,attractionId,date,time,price) VALUES (%s,%s,%s,%s,%s)"
      val = (email,attractionId,date,time,price)
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql,val)
      conn.commit()
      if newCursor.rowcount == 1 :
         return "insertDone"
      else:
         return "insertError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def delete_booking(email):
   try:
      sql="DELETE FROM booking WHERE email='"+email+"'"
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql)
      conn.commit()
      if newCursor.rowcount == 1 :
         return "deleteDone"
      else:
         return "deleteError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

### Order ###
def insert_order(**kwargs):
   try:
      sql="INSERT INTO orders(number,name,email,phone,attId,datetime,time,price,paystatus,bank_transaction_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val=(kwargs["number"],kwargs["username"],kwargs["email"],kwargs["phone"],kwargs["attId"],kwargs["tripdate"],kwargs["triptime"],kwargs["price"],kwargs["paystatus"],kwargs["bank_transaction_id"])
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql,val)
      conn.commit()
      if newCursor.rowcount == 1 :
         return "insertDone"
      else:
         return "insertError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def update_order(**kwargs):
   try:
      sql="UPDATE orders SET paystatus='"+kwargs["paystatus"]+"',bank_transaction_id='"+kwargs["bank_transaction_id"]+"' WHERE number='"+kwargs["number"]+"'"
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql)
      conn.commit()
      if newCursor.rowcount == 1 :
         return "updateDone"
      else:
         return "updateError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def select_order(num):
   try:
      sql="SELECT number,name,email,phone,attId,datetime,time,price FROM orders WHERE number='"+num+"'"
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql)
      myResult = newCursor.fetchone()
      if myResult != None:
         data = dict(zip(newCursor.column_names,myResult))
         return data
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)

def insert_travel_data(**kwargs):
   try:
      sql = "INSERT INTO travel(id,info,stitle,xpostDate,longitude,REF_WP,avBegin,langinfo,MRT,SERIAL_NO,RowNumber,CAT1,CAT2,MEMO_TIME,POI,file,idpt,latitude,xbody,avEnd,address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (kwargs["id"],kwargs["info"],kwargs["stitle"],kwargs["xpostDate"],kwargs["longitude"],kwargs["REF_WP"],kwargs["avBegin"],kwargs["langinfo"],kwargs["MRT"],kwargs["SERIAL_NO"],kwargs["RowNumber"],kwargs["CAT1"],kwargs["CAT2"],kwargs["MEMO_TIME"],kwargs["POI"],kwargs["file"],kwargs["idpt"],kwargs["latitude"],kwargs["xbody"],kwargs["avEnd"],kwargs["address"])
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql,val)
      conn.commit()
      if newCursor.rowcount == 1 :
         return "insertDone"
      else:
         return "insertError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)


###############AWS_RDS_POST_DATA
def rds_insertdata(**kwargs):
   try:
      sql = "INSERT INTO postdata(description,pic) VALUES(%s,%s)"
      val = (kwargs["imgtxt"],kwargs["imgpath"])
      conn = conn_pool.get_connection()
      newCursor=conn.cursor()
      newCursor.execute(sql,val)
      conn.commit()
      if newCursor.rowcount == 1 :
         return "insertDone"
      else:
         return "insertError"
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(conn, newCursor)


   







   



