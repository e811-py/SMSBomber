import pymongo

con = pymongo.MongoClient('127.0.0.1', 27017)
db1 = con['SMSBomber']
col1 = db1['Users']
# db2 = con['SMSBomberV2']
# col2 = db2['Users']


col1.update_many({'VipMode':False}, {'$set':{'VipMode':{'pay':False, 'End':'', 'date':''}}})
col1.update_many({'VipMode':True}, {'$set':{'VipMode':{'pay':True, 'End':'Never', 'date':''}}})

for i in col1.find(): print(i)

# for user in col1.find():
#     if user['VipMode']:
#
