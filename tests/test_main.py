import pytest
from src.main import summarize_email, ask_question
from unittest.mock import patch, MagicMock  
from src.main import app;

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('src.main.OpenAI')
def test_summarize_endpoint(mock_openai, client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mock summary"))]
    mock_openai.return_value.chat.completions.create.return_value = mock_response

    # Test request
    response = client.post('/summarize', json={'email_text': 'test content'})
    
    assert response.status_code == 200
    assert 'Mock summary' in response.json['summary']


# Auto-generated tests
def test_summarize_email_no_email_text(client):
    response = client.post('/summarize', json={})
    assert response.status_code == 400

def test_summarize_email_with_email_text(client):
    response = client.post('/summarize', json={'email_text': 'This is a test email.'})
    assert response.status_code == 200
    assert 'summary' in response.json

def test_ask_question_no_document_text(client):
    response = client.post('/ask', json={'question': 'What is the answer?'})
    assert response.status_code == 400

def test_ask_question_no_question(client):
    response = client.post('/ask', json={'document_text': 'This is a test document.'})
    assert response.status_code == 400

def test_ask_question_with_document_text_and_question(client):
    response = client.post('/ask', json={'document_text': 'This is a test document.', 'question': 'What is the answer?'})
    assert response.status_code == 200
    assert 'answer' in response.json