import boto3
import cf_response
import time
import uuid
 
def handler(event, context):
    try:
        # This automatically succeeds when the custom resource is called during deletion
        # It uses the cf_response file which 
        if event['RequestType'] == 'Delete':
            cf_response.send(event, context, 'SUCCESS', {'Status': 'SUCCESS'})
            return 'SUCCESS'
        # This is the real core 'custom' part of this custom resource
        # All it does it write 10 test items to a DynamoDB table
        # But you can really do anything supported by the AWS SDKs
        i = 0
        while i < 10:
            i = i + 1
            clients_table = boto3.resource('dynamodb').Table('Clients')
            clients_table.put_item(
                Item={
                    'ClientId': str(uuid.uuid4()),
                    'paymentStatus': random.choice(['paid', 'overdue', 'canceled'])
                }
            )
            # Wait a little because the table only has 5 write capacity units
            time.sleep(0.25)
        # If all this works... 
        # Then return response to CloudFormation saying this was successful
        cf_response.send(event, context, 'SUCCESS', {'Status': 'SUCCESS'})
    except Exception as e:
        # Return a failure to CloudFormation if there's an error in the process above
        print(str(e))
        cf_response.send(event, context, 'FAILED', {'Status': 'FAILED'})