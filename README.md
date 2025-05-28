# AI Assistant MVP

This is a scaffold for an AI assistant backend that integrates:
- Email parsing with OpenAI GPT-4
- Task management with Basecamp API
- Purchase order creation with SAP Business One REST API
- WhatsApp messaging for follow-ups

## Setup

1. Set your API keys in `app/config.py`
2. Build and run with Docker or directly using Python
3. Deploy on cloud platforms like Render or AWS

## API

- POST `/email` with JSON payload `{ "body": "email text here" }`
