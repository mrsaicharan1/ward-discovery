import boto3

def schema_providers_gen():
    dynamodb = boto3.resource('dynamodb')

    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='provider',
        KeySchema=[
            {
                'AttributeName': 'provider_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'provider_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='provider')

    # Print out some data about the table.
    print(table.item_count)

def schema_seekers_gen():
    dynamodb = boto3.resource('dynamodb')

    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='seeker',
        KeySchema=[
            {
                'AttributeName': 'seeker_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'seeker_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='providers')

    # Print out some data about the table.
    print(table.item_count)

def schema_ward_gen():
    dynamodb = boto3.resource('dynamodb')

    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='ward',
        KeySchema=[
            {
                'AttributeName': 'ward_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ward_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='ward')

    # Print out some data about the table.
    print(table.item_count)

schema_ward_gen()