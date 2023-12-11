import json
import boto3
from datetime import datetime
import logging
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions as es_exceptions
from requests_aws4auth import AWS4Auth

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))

    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    logger.info(f"Processing S3 object - Bucket: {s3_bucket}, Key: {s3_key}")

    # Detect labels in the image using Rekognition
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
        MaxLabels=10,
        MinConfidence=70
    )
    labels = [label['Name'] for label in response['Labels']]

    # Retrieve S3 metadata
    s3_client = boto3.client('s3')
    metadata_response = s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
    metadata = metadata_response.get('Metadata', {})
    # Extracting custom labels and handling comma-separated values
    custom_labels_str = metadata.get('customlabels', '')
    if custom_labels_str:
        # Splitting the string by commas to get individual labels
        custom_labels = custom_labels_str.split(',')
    else:
        custom_labels = []
    
    print("custom labels: " + str(custom_labels))
    # logger.info(f"Retrieved metadata: {metadata}")
    # custom_labels = json.loads(metadata.get('customlabels', '[]'))
    # print("custom labels: " + str(custom_labels))

    labels.extend(custom_labels)

    # Log combined labels
    logger.info(f"Combined labels: {labels}")

    # Create ElasticSearch JSON object
    es_object = {
        'objectKey': s3_key,
        'bucket': s3_bucket,
        'createdTimestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
        'labels': labels
    }

    # Elasticsearch connection and indexing
    es_endpoint = 'search-photos-w6cb2glnjaqfxa47x2zgho6ore.us-east-1.es.amazonaws.com'
    es_index = 'photos'
    es_client = Elasticsearch(
        hosts=[{'host': es_endpoint, 'port': 443}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        http_auth=('Masterphotos', 'Photos@123')  # Ensure these credentials are secured
    )

    try:
        es_client.index(
            index=es_index,
            body=json.dumps(es_object),
            doc_type='_doc',
            id=s3_key
        )
    except es_exceptions.RequestError as e:
        logger.error(f"Error indexing document in Elasticsearch: {e}")

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json'
        },
        'body': json.dumps("Image labels have been successfully detected and processed!")
    }