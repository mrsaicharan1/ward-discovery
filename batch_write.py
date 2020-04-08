import boto3
from helpers import generate_uuid

def batch_write_ddb(provider_id='3123', wards_list=[1,2,3,4,5,6,7]):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ward')
    with table.batch_writer() as batch:
        for ward_id in wards_list:
            batch.put_item(
                Item={
                    'ward_id': ward_id,
                    'status': False,
                    'provier_id': provider_id,
                }
            )
    return 1

batch_write_ddb()