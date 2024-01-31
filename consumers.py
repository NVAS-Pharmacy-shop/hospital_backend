import datetime
import json
import time

import pika

from hospital_contract.models import Contract
from hospital_contract.tasks import send_delivered_equipment_to_rabbitmq


def callback(ch, method, properties, body):
    contract_data = json.loads(body)

    contract = Contract.objects.filter(id=contract_data).first()
    contract.status = 'delivering'
    contract.date += datetime.timedelta(days=30)
    contract.save()
    print("SELI")
    time.sleep(5)
    print("SELI")
    contract.status = 'active'
    contract.save()
    send_delivered_equipment_to_rabbitmq(contract.id)

def callback1(ch, method, properties, body):
    contract_data = json.loads(body)

    contract = Contract.objects.filter(id=contract_data).first()
    contract.status = 'cancelled'
    contract.date += datetime.timedelta(days=30)
    contract.save()

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='equipment_delivery')
    channel.queue_declare(queue='contract_cancellation')

    channel.basic_consume(queue='equipment_delivery', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='contract_cancellation', on_message_callback=callback1, auto_ack=True)

    print('Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()