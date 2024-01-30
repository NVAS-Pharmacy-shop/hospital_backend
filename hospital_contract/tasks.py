import json
import pika
from hospital_contract.models import Contract

def send_contract_to_rabbitmq(contract_id):
    try:
        contract = Contract.objects.get(id=contract_id)

        contract_data = {
            'hospital_id': contract.hospital_id,
            'date': contract.date.strftime('%Y-%m-%d,%H:%M:%S'),
            'company': contract.company,
            'equipment': [{'equipment_id': equipment.equipment_id, 'quantity': equipment.quantity} for equipment in
                          contract.equipment.all()]
        }
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='contract_requests')
        channel.basic_publish(exchange='', routing_key='contract_requests', body=json.dumps(contract_data))

        print("Contract sent to RabbitMQ")

        connection.close()
    except Contract.DoesNotExist:
        print(f"Contract with id {contract_id} does not exist.")
