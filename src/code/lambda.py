import json
import requests
import os

def main(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        process_sqs_message(message_body)
        return notify_payments(message_body)

def process_sqs_message(message_body):
    print("Processing SQS message:")
    print("Body:", message_body)

def notify_payments(body):
    order_id = body['order_id']

    url_base = os.environ['URL_BASE']
    port = os.environ['PORT']
    endpoint = os.environ['ENDPOINT'].replace('id_pedidos', order_id)

    url = url_base + ':' + port +  '/' + endpoint
    print('REQUEST URL: ', url)

    try:
        #response = requests.get(url, data=json.dumps(body), headers={'Content-Type': 'application/json'})
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        print('Response: ', response.json())

        if response.status_code > 199 and response.status_code < 300:
            return {
                'statusCode': response.status_code,
                'body': json.dumps('Pedido {order_id} Message processed successfully!')
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps('Pedido {order_id} Message Error!')
            }
    except Exception as e:
        print('Exception error: ', e)
        return {
            'statusCode': 500,
            'body': json.dumps('Pedido {order_id} Message Exception Error!')
        }