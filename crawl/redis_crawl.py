from redis import StrictRedis,ConnectionPool

# 通过url构造
url='redis://:217217@localhost:6379/0'
pool=ConnectionPool.from_url(url)

# redis=StrictRedis(host='localhost',port=6379,db=0,password='217217')
redis=StrictRedis(connection_pool=pool)
redis.set('tom','lisi')
print(redis.get('name'))
print(type(redis.get('name')))
print(redis.dbsize())