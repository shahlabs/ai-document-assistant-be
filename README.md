This is a python project which uses flask and is backend to [https://github.com/shahlabs?tab=repositories
](https://github.com/shahlabs/ai-document-assistant)
It uses OpenAI to get the summary of the email and answer the question related to document uploaded by user. 

# Project setup

Install dependencies
```bash
poetry install
```

## OpenAI setup

1. Create an API key at https://platform.openai.com/account/api-keys
2. Save as environment variable under `OPENAI_API_KEY` in .env file at top folder

## How to run it 
```bash
cd src
python3 main.py
(or python main.py depending on your installation)
```
## Testing Endpoints

The endpoints can be tested using curl or postman

```
curl --location 'http://localhost:5000/summarize' \
--header 'Content-Type: application/json' \
--data '{
    "email_text": "Dear Team, Please be informed that tomorrow'\''s meeting has been rescheduled to Friday at 2 PM EST due to conflicts with the product launch. Kindly review the updated agenda document attached and confirm  your attendance by EOD today.Best regards,Sarah"
}'

curl --location 'http://localhost:5000/ask' \
--header 'Content-Type: application/json' \
--data '{
    "document_text": "Server reboots occur every Sunday 3AM GMT. Maintenance window lasts 4 hours.",
    "question": "When is maintenance scheduled?"
  }'
```
