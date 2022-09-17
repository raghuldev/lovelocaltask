#from crypt import methods
from urllib import request
from flask import Flask, request, jsonify
from loveLocal import loveLocal
import json

app = Flask(__name__)
ll = loveLocal()

@app.route("/")
def home():
    return "Hello World"

@app.route("/saveCustData")
def saveCustData():
    ll.sendDataToDB()
    return "Sucess"

@app.route("/submit")
def submit():
    return "Hello from submit page"

@app.route("/fetchOrderId", methods=["GET"])
def fetchOrderId():
    args = request.args
    orderId = args.get("orderid", default=0, type=int)
    if orderId != 0:
        res = ll.fetchOrderData(orderId)
        res = json.dumps(res)
        return res 
    else:
        return "Invalid Order Id!"

@app.route("/fetchAvgNoProds", methods=["GET"])
def fetchAvgNoProds():
    return str(ll.fetchAvgNoProds())
    #return "AVG >>>"

@app.route("/fetchProdAvg", methods=["GET"])
def fetchProdAvg():
    args = request.args
    prodId = args.get("prodId", default=0, type=int)
    if prodId != 0:
        res = ll.fetchAvgQnProd(prodId)
        res = json.dumps(res)
        return res 
    else:
        return "Invalid Order Id!"


if __name__ == '__main__':
    app.run()
