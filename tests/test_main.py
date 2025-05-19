import pytest
from src.main import summarize_email, ask_question
from unittest.mock import patch, MagicMock  
from src.main import app;

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_summarize_missing_email_text(client):
    """Test missing email_text returns 500 Bad Request"""
    response = client.post('/summarize', json={})
    assert response.status_code == 500


# Auto-generated tests
def test_summarize_email_no_text(client):
    response = client.post('/summarize', json={'email_text': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'No email text provided'

def test_summarize_email_with_text(client):
    response = client.post('/summarize', json={'email_text': 'This is a sample email.'})
    assert response.status_code == 200
    assert 'summary' in response.json

def test_ask_question_no_text(client):
    response = client.post('/ask', json={'document_text': '', 'question': 'What is this about?'})
    assert response.status_code == 400
    assert response.json['error'] == 'No document text or question provided'

def test_ask_question_no_question(client):
    response = client.post('/ask', json={'document_text': 'This is a document.', 'question': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'Question is required'

def test_ask_question_with_text_and_question(client):
    response = client.post('/ask', json={'document_text': 'This is a document.', 'question': 'What is this about?'})
    assert response.status_code == 200
    assert 'answer' in response.json