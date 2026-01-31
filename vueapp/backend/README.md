# Bedrock Knowledge Base Backend

This is a FastAPI-powered backend that acts as a secure proxy for calling Amazon Bedrock Knowledge Base.

## Setup

1. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file (see `.env.example` for reference):
   ```env
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   KNOWLEDGE_BASE_ID=your_kb_id
   BEDROCK_MODEL_ARN=arn:aws:bedrock:ap-southeast-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0
   ```

## Running the Server

```bash
uvicorn main:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `POST /chat`: Send a query to the Knowledge Base.
  - Body: `{ "query": "your question" }`
- `GET /health`: Health check endpoint.
