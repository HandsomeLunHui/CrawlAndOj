import pika
import requests
import pickle

# 生产者模型
# 设置队列名称
QUEUE_NAME='scrape'
TOTAL=100
MAX_PRIORITY=10
# 连接rabbitmq服务
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# 获取一个channel对象
channel = connection.channel()
# 声明请求队列 queue=队列名称
channel.queue_declare(queue=QUEUE_NAME,durable=False)
# 生产消息到请求队列中
# channel.basic_publish(exchange='',routing_key=QUEUE_NAME,body="你好")

for i in range(1,TOTAL+1):
    url=f'https://ssr1.scrape.center/detail/{i}'
    # 构造请求对象
    request=requests.Request('GET',url)
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=pickle.dumps(request),
                          properties=pika.BasicProperties(delivery_mode=2))
    print(f"put {url}")

# while True:
#     data=input()
#     channel.basic_publish(exchange='',routing_key=QUEUE_NAME,body=data)
#     print(f"put {data}")