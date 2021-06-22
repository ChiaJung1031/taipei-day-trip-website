from flask import Blueprint
from flask import *
from model.booking import newbook,getbook,deletebook

booking_api = Blueprint('booking_api', __name__)


@booking_api.route("/api/booking",methods=["POST"])
def newbooking():
    postdata = request.json
    data = newbook(postdata)
    return data



@booking_api.route("/api/booking",methods=["GET"])
def getbooking():
    mail = session.get('email')  
    name = session.get('name')
    data=getbook(mail,name)
    return data

    
@booking_api.route("/api/booking",methods=["DELETE"])
def deletebooking():
    mail = session.get('email') 
    data = deletebook(mail)
    return data
