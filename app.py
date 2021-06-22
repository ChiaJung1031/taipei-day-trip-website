from flask import *
from datetime import timedelta
from routes.user import user_api
from routes.attraction import attraction_api
from routes.booking import booking_api
from routes.order import order_api
from routes.upload import upload_api

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

@app.route("/upload")
def upload():
	return render_template("upload.html")

@app.route("/loaderio-2ce70f20c355a778c557d5ec6a9090a6")
def uploadtest():
	return render_template("loaderio-2ce70f20c355a778c557d5ec6a9090a6.html")

app.register_blueprint(user_api)
app.register_blueprint(attraction_api)
app.register_blueprint(booking_api)
app.register_blueprint(order_api)
app.register_blueprint(upload_api)

app.run(host="0.0.0.0",port=3000)