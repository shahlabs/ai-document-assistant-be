from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv;
from flask import Flask, request, jsonify
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/summarize', methods=['POST'])
def summarize_email():
    """
    Endpoint to handle email summarization requests
    Expected JSON payload: {'email_text': '...'}
    """
    try:
        data = request.get_json()
        email_text = data.get('email_text', '')

        if not email_text:
            return jsonify({'error': 'No email text provided'}), 400
        
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': ''' You are an expert email summarizer. Create concise summaries that highlight:
                 - Key requests/actions
                 - Urgency level
                 - Main topics
                 Keep under 3 sentences.'''},
                {'role': 'user', 'content': f"Please summarize the following email: '{email_text}'"},
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        summary = response.choices[0].message.content
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        document_text = data.get('document_text', '').strip()
        question = data.get('question', '').strip()

        if not document_text:
            return jsonify({'error': 'No document text or question provided'}), 400
        if not question:
            return jsonify({'error': 'Question is required'}), 400

        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': f'''
                    Answer questions based on this document:
                    {document_text[:3000]}  # Limit to first 3000 chars
                    If the question can't be answered, say "Not covered in the document"
                '''},
                {'role': 'user', 'content': f"Question: '{question}'"},
            ],
            temperature=0.3,
            max_tokens=500
        )

        answer = response.choices[0].message.content
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)