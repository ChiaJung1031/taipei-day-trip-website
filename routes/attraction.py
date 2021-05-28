from flask import Blueprint
from flask import *
from model.attraction import getdata,getattractid

attraction_api = Blueprint('attraction_api', __name__)



@attraction_api.route("/api/attractions",methods=['GET', 'POST'])
def apiattract():
    page=request.args.get("page","0")
    keyword=request.args.get("keyword","")
    data = getdata(page,keyword)
    return data
	


@attraction_api.route("/api/attraction/<attractionId>",methods=["GET"])
def apiattractid(attractionId):
    id=attractionId
    data = getattractid(id)
    return data

	
