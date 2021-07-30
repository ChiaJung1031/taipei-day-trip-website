from flask import Blueprint,request,json
from flask import *
from sql_database import *
from model.upload import *
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

cdn_path = os.getenv("CLOUDFRONT_PATH")
file_extension = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
upload_api = Blueprint('upload_api', __name__)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in file_extension

@upload_api.route("/load",methods=["POST"])
def new():
    if "image" in request.files:
        image = request.files["image"]
        letter = request.form["letter"]
        if image and allowed_file(image.filename):
            image.filename = secure_filename(image.filename)
            imagestatus = upload_to_aws(image, 'bucketweek1')
            if imagestatus == "uploadOK":
                img_path="https://"+cdn_path +"/" + image.filename
                insertdata = rds_insertdata(imgpath=img_path,imgtxt=letter)
                if insertdata=="insertDone":
                    data = {"error": None, "data": {"img_txt":letter , "imgurl":img_path }}
                    return jsonify(data)
                else:
                    return jsonify({ "error": True, "message": "資料庫輸入有誤" })
            else:
                jsonify({ "error": True, "message": "上傳檔案錯誤" })
    else:
        return jsonify({ "error": True, "message": "未選取檔案" })


@upload_api.route("/api/load",methods=["GET"])
def getupload():
    data=getalldata()
    if data != "NoData":
        data_list = []
        for i in data:
            every_data={
                "id":i[0],
                "letter":i[1],
                "imgurl":i[2]
            }
            data_list.append(every_data)
        alldata={"data":data_list}
        return alldata
    else:
        return "NoData"








