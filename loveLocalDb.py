from pymongo import MongoClient
from pymongo.write_concern import WriteConcern

def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return wrapper

@singleton
class localLocalDB:
    db = None
    client = None
    def __init__(self) -> None:
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["users"]
        self.loveLocalOrdersCollection = None
        self.createCollections()
    
    def getDB(self):
        return self.db

    def createCollections(self):
        #create users collection
        self.loveLocalOrdersCollection = self.db['orders']
        self.loveLocalOrdersCollection.create_index('order_id', unique=True, background=True)
    
    def saveOrders(self, orderData):
        #handling duplicate entries
        self.loveLocalOrdersCollection.with_options(write_concern=WriteConcern(w=0)).insert_many(orderData, ordered=False)
        print("Order Data Saved in Users Collections")
    
    def getAllOrders(self):
        data = []
        for d in self.loveLocalOrdersCollection.find():
            data.append(d)
        return data
    
    def getOrderByID(self, id):
        query = {'order_id': id}
        res = self.loveLocalOrdersCollection.find_one(query)
        if res != None:
            del res['_id']
        if res == None:
            res = []
        return res
    
    def getAllProductCounts(self):
        query = {'product_count':1}
        prodCounts = []
        res = self.loveLocalOrdersCollection.find({}, query)
        if res == None:
            return prodCounts
        for i in res:
            prodCounts.append(i['product_count'])
        return prodCounts
    
    def getProdQuantAllOrders(self, prodId):
        #res = self.loveLocalOrdersCollection.aggregate([ { "$unwind": "$products" }, { "$match": { "products.id": prodId } }, { "$group": { "_id": "$products.id", "avg": { "$avg": "$products.quantity" }, "name": { "$first": "$$ROOT.products.name" }, "measurement": { "$first": "$$ROOT.products.measurement" }, "productId": { "$first": "$$ROOT.products.id" } } }])
        res = self.loveLocalOrdersCollection.aggregate([ { "$unwind": "$products" }, { "$match": { "products.id": prodId } }, { "$group": { "_id": "$products.id", "avg": { "$push": "$products.quantity" }, "name": { "$first": "$$ROOT.products.name" }, "measurement": { "$first": "$$ROOT.products.measurement" }, "productId": { "$first": "$$ROOT.products.id" } } }])
        res = list(res)
        return res