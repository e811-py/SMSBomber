import pymongo
import sqlite3

MongoConnect = pymongo.MongoClient("localhost", 27017)
MDB = MongoConnect['SMSBomber']
MDB_Users = MDB['Users']

SqliteConnect = sqlite3.connect('BombDB.db', check_same_thread=False)
SDB = SqliteConnect.cursor()

for data in SDB.execute(''' SELECT * FROM Users '''):
    # print(data)
    if data[2] == '0': vipT=False
    elif data[2] == '1': vipT=True
    if data[5] == '0': vip=False
    elif data[5] == '1': vip=True
    if data[6] == '0': ban=False
    elif data[6] == '1': ban=True

    # MDB_Users.insert_one({"_id":int(data[0]), "Username":data[1], "PhoneNumbers":[data[3]], "Subset":int(data[4]), "VipMode":vip, "TestVip":vipT, "Ban":ban, "lastF":{}, "lastLoc":""})
    MDB_Users.insert_one({"_id":int(data[0]), "Username":data[1], "Requests":[], "Subset":int(data[4]), "VipMode":vip, "TestVip":vipT, "Ban":ban, "lastF":{}, "lastLoc":"main_menu"})
print('result: ')

for i in MDB_Users.find():
    print(i)

