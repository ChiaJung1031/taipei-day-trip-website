from flask import Blueprint
from flask import *
from model.user import signup,signin,checkuser,deleteuser

user_api = Blueprint('user_api', __name__)


@user_api.route("/api/user",methods=["POST"])
def apiusersignup():
	password=request.args.get("password","")
	email=request.args.get("email","")
	username=request.args.get("name","")
	data = signup(password,email,username)
	return data


@user_api.route("/api/user",methods=["PATCH"])
def apiusersignin():
	password=request.args.get("password","")
	email=request.args.get("email","")
	data = signin(password,email)
	return data
	

@user_api.route("/api/user",methods=["GET"])
def apiusercheck():
	id = session.get('id') 
	email = session.get('email')
	name = session.get('name')
	data = checkuser(id,email,name)
	return data
	

@user_api.route("/api/user",methods=["DELETE"])
def apiuserlogout():
	data = deleteuser()
	return data

			