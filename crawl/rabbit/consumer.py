import pika
import requests
import pickle


# 消费者模型
QUEUE_NAME = 'scrape'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
session=requests.Session()
channel.queue_declare(queue=QUEUE_NAME)

def scrape(request):
    try:
        response=session.send(request.prepare())
        print(f'success scraped {response.url}')
    except Exception as e:
        print(f'failed scraped {request.url}')


while True:
    method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME,auto_ack=True)
    if body:
        # bytes 类型解码为中文 bytes.decode('utf-8')
        request=pickle.loads(body)
        print(f"Received {request}")
        scrape(request)

#
# # 回调函数
# def callback(ch, method, properties, body):
#     print(f"Received {body}")
#
# while True:
#     input("Press Enter to continue...")
#     method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME,auto_ack=True)
#
#     if body:
#         # bytes 类型解码为中文 bytes.decode('utf-8')
#         print(f"Received {body}")

# channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
# channel.start_consuming()