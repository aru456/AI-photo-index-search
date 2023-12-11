import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

def lambda_handler(event, context):
    # Extract the query text from the event
    print("Changed the code and printing in logs")
    query_text = event['queryStringParameters']['q']

    # Set up the Lex V2 client
    lex_client = boto3.client(
        'lexv2-runtime',
        region_name='us-east-1',
        aws_access_key_id='AKIAZTLLAHQ76HX5XZY7',
        aws_secret_access_key='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'
    )

    botId = "ZHLYN52ECD"
    botAliasId = "TSTALIASID"
    localeId = "en_US"
    sessionId = "100"

    # Send the query text to Lex
    lex_response = lex_client.recognize_text(
        botId=botId,
        botAliasId=botAliasId,
        localeId=localeId,
        sessionId=sessionId,
        text=query_text
    )
    print("-------------lex_response----------")
    print(lex_response)

    # Extract keywords from Lex response
    # keywords = []  # Modify this to extract relevant information from lex_response
    
    slots = lex_response['sessionState']['intent']['slots']
    keywords = [slots[slot]['value']['originalValue'] for slot in slots if slots[slot] and 'value' in slots[slot]]

    print(keywords)
    
    es_endpoint = 'search-photos-w6cb2glnjaqfxa47x2zgho6ore.us-east-1.es.amazonaws.com'  # Corrected the Elasticsearch endpoint
    

    es_client = Elasticsearch(
        hosts=[{'host': es_endpoint, 'port': 443}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        http_auth=('Masterphotos', 'Photos@123')
    )
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }

    # Perform the search on ElasticSearch
    if keywords:
        search_query = " OR ".join(keywords)
        es_response = es_client.search(
            index='photos',
            body={"query": {"match": {"labels": search_query}}}
        )
        print("es_response")
        print(es_response)
        
        es_hits = es_response['hits']['hits']

        s3_bucket_url = "https://photos-bucket-ass3.s3.amazonaws.com/"
        img_list = [s3_bucket_url + hit['_id'] for hit in es_hits]

        print(img_list)
        
        lex_client.delete_session(botId=botId,botAliasId=botAliasId,localeId=localeId,sessionId=sessionId)
        
        # Format the response as required
        if img_list:
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    'Content-Type': 'application/json'
                },
                'body': json.dumps(img_list)
            }
        else:
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    'Content-Type': 'application/json'
                },
                'body': json.dumps("No such photos.")
            }
    else:
        # Return an empty array if no keywords
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                'Content-Type': 'application/json'
            },
            'body': json.dumps("error in code")
        }