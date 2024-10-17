# PhotoFind AI

### Project Description
**PhotoFind AI** is an intelligent image search platform built using AWS services. The system allows users to upload images, which are indexed and made searchable through both custom labels and AI-generated tags. By leveraging AWS Lambda, Rekognition, Elasticsearch (OpenSearch), and Lex Bot, the platform enables seamless image search capabilities using simple keyword-based queries.

### Workflow
1. **Image Upload to S3**:
   - Users upload images with custom labels, which are stored in an Amazon S3 bucket.

2. **Trigger Lambda Function**:
   - The image upload triggers an AWS Lambda function that invokes AWS Rekognition to generate labels. Both AI-generated and custom labels are then indexed in Elasticsearch.

3. **Search Query**:
   - Users submit search phrases, such as "show me a tiger." The Amazon Lex Bot processes the phrase and extracts keywords like "tiger."

4. **Elasticsearch Query**:
   - The extracted keywords are used to search the Elasticsearch index for matching images.

5. **Results Display**:
   - URLs of matching images from S3 are retrieved and displayed in the user’s browser.

### Technologies Used
- **AWS Lambda**: Backend processing and event-driven architecture.
- **Amazon S3**: Storage for user-uploaded images.
- **Amazon Rekognition**: Image analysis and label generation.
- **Elasticsearch (OpenSearch)**: Indexing and searching of labels.
- **Amazon Lex Bot**: Extracting keywords from user search queries.
- **API Gateway**: Handling API requests.

### Demo
[Watch the demo on YouTube](https://youtu.be/3m-8Km6NOmc)
