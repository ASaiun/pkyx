import pymongo
conn = pymongo.Connection(host='127.0.0.1', port=27017)
print(conn)
