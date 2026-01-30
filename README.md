# Bedrock Doc Assistant

A Streamlit application for interacting with Amazon Bedrock's knowledge base for assistance based on docs uploaded.

## Features

- Chat interface with Amazon Bedrock
- Knowledge base integration using `retrieve_and_generate`
- Configuration sidebar for API keys and knowledge base ID
- Session management for chat history

## Setup

1. Activate the virtual environment:
```bash
source app/venv/bin/activate
```

2. Create the virtual environment and install dependencies:
```bash
python -m venv app/venv
source app/venv/bin/activate
pip install -r app/requirements.txt
```

3. Configure your secrets:
```bash
mkdir -p app/.streamlit
cp app/.streamlit/secrets.example app/.streamlit/secrets.toml
```

4. Edit `app/.streamlit/secrets.toml` with your actual values:
```toml
AWS_ACCESS_KEY_ID = "your-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
AWS_SESSION_TOKEN = "" # optional
KNOWLEDGE_BASE_ID = "your-knowledge-base-id"
BEDROCK_MODEL_ARN = "arn:aws:bedrock:ap-southeast-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
```

5. Create access keys in AWS (if you don't already have them):
   - AWS Console → IAM → Users → your user → Security credentials
   - Create access key → choose "Application running outside AWS"
   - Copy the Access key ID and Secret access key into `app/.streamlit/secrets.toml`

## Running the App

```bash
cd app
source venv/bin/activate
streamlit run app.py
```

## Configuration

You can configure the app through:
- The sidebar UI (recommended for testing)
- `.streamlit/secrets.toml` file (recommended for production)
- Environment variables

## Notes

- The app uses the `retrieve_and_generate` API method
- Region is set to `ap-southeast-2`
- Uses Claude 3 Haiku model by default
- Authentication uses AWS access key and secret
- The CDK stack creates a VPC with private subnets and adds VPC endpoints for
  Bedrock, Bedrock Runtime, Bedrock Agent, Bedrock Agent Runtime, S3, and
  OpenSearch Serverless to enable private networking where supported.
- Knowledge Bases are managed services and do not run inside your VPC; private
  connectivity is achieved via VPC endpoints for your clients and (optionally)
  your OpenSearch Serverless collection.
- If your OpenSearch Serverless collection is private, ensure its network
  policy allows the VPC endpoint created by this stack and the Bedrock service
  role has access to the collection.
