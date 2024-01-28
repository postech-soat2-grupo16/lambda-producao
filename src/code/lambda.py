import json
import requests
import os

def main(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        process_sqs_message(message_body)
        return notify_production(message_body)

def process_sqs_message(message_body):
    print("Processing SQS message:")
    print("Body:", message_body)

def notify_production(body):
    order_id = body['PedidoID']

    url_base = os.environ['URL_BASE']
    port = os.environ['PORT']
    endpoint = os.environ['ENDPOINT'].replace('order_id', order_id)

    url = url_base + ':' + port +  '/' + endpoint
    print('REQUEST URL: ', url)

    try:
        response = requests.patch(url, data=json.dumps(body), headers={'Content-Type': 'application/json'})
        print('Response: ', response.json())

        if response.status_code > 199 and response.status_code < 300:
            return {
                'statusCode': response.status_code,
                'message': 'Pedido Atualizado com sucesso!',
                'body': body
            }
        else:
            return {
                'statusCode': response.status_code,
                'message': 'Erro ao atualizar pagamento',
                'body': body
            }
    except Exception as e:
        print('Exception error: ', e)
        return {
            'statusCode': 500,
            'message': 'Exception error!',
            'body': body
        }