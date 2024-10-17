Project Description
The AI Photo Index Search system is an intelligent image search platform built using AWS services. It allows users to upload images, which are indexed and searchable through custom labels and AI-generated tags. Leveraging AWS Lambda, Rekognition, Elasticsearch (OpenSearch), and Lex Bot, this platform provides a seamless user experience for querying images by keywords and metadata.

Workflow
Image Upload to S3:
Users upload images along with custom labels, and these are stored in an S3 bucket.

Trigger Lambda Function:
The image upload triggers a Lambda function, which uses AWS Rekognition to generate labels from the image and stores both AI-generated and custom labels in Elasticsearch.

Search Query:
Users can input search queries, such as "show me a tiger". These phrases are processed through an Amazon Lex Bot, which extracts keywords like "tiger".

Elasticsearch Query:
The extracted keywords are used to search the Elasticsearch index for matching images.

Results Display:
URLs of matching images stored in S3 are retrieved and rendered in the user’s browser for easy viewing.

Technologies Used
Lambda Functions for backend processing
Amazon S3 for image storage
Amazon Rekognition for image labeling
Elasticsearch (OpenSearch) for index and search functionality
API Gateway for handling API requests
Amazon Lex Bot for keyword extraction from search phrases

Youtube Demo Link - https://youtu.be/3m-8Km6NOmc
