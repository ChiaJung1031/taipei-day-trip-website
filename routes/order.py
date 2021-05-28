from flask import Blueprint
from flask import *
from model.order import neworder,getorder

order_api = Blueprint('order_api', __name__)

@order_api.route("/api/orders",methods=["POST"])
def neworders():
    postdata = request.json
    data = neworder(postdata)
    return data


@order_api.route("/api/orders/<orderNumber>",methods=["GET"])
def getorders(orderNumber):
    num=orderNumber
    data = getorder(num)
    return data