import urllib.request
import json
from loveLocalDb import localLocalDB
from utils import loveUtils

DATA_STORE_LINK = "https://orders-staging-api-fc7lwmf3uq-el.a.run.app/orders/all"

class loveLocal:
    def __init__(self) -> None:
        self.lovedb = localLocalDB()

    def fetchRawData(self):
        with urllib.request.urlopen(DATA_STORE_LINK) as url:
            raw = json.loads(url.read())
            return raw
    
    def sendDataToDB(self):
        rawData = self.fetchRawData()
        orderCount = rawData['count']
        orderData = rawData['data']
        print("DATA TO DB")
        self.lovedb.saveOrders(orderData)
        print(self.lovedb.getAllOrders())
    
    def fetchOrderData(self, orderId):
        return self.lovedb.getOrderByID(orderId)
    
    def fetchAvgNoProds(self):
        #get product count from all orders
        productCounts = self.lovedb.getAllProductCounts()
        #finding median from productcounts list
        return loveUtils.findMedian(productCounts)
    
    def fetchAvgQnProd(self, prodId):
        return self.lovedb.getProdQuantAllOrders(prodId)
        

