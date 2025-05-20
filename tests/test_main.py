import pytest
from src.main import summarize_email, ask_question
from unittest.mock import patch, MagicMock  
from src.main import app;
from flask import json

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
@patch('src.main.OpenAI')
def test_summarize_email(mock_openai, client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="..."))]
    mock_openai.return_value.chat.completions.create.return_value = mock_response
    response = client.post('/summarize', json={'email_text': 'Test email text'})
    assert response.status_code == 200
    assert 'summary' in response.json

@patch('src.main.OpenAI')
def test_summarize_email_no_text(mock_openai, client):
    response = client.post('/summarize', json={'email_text': ''})
    assert response.status_code == 400
    assert 'error' in response.json

@patch('src.main.OpenAI')
def test_ask_question(mock_openai, client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="..."))]
    mock_openai.return_value.chat.completions.create.return_value = mock_response
    response = client.post('/ask', json={'document_text': 'Test document', 'question': 'Test question'})
    assert response.status_code == 200
    assert 'answer' in response.json

@patch('src.main.OpenAI')
def test_ask_question_no_text(mock_openai, client):
    response = client.post('/ask', json={'document_text': '', 'question': 'Test question'})
    assert response.status_code == 400
    assert 'error' in response.json

@patch('src.main.OpenAI')
def test_ask_question_no_question(mock_openai, client):
    response = client.post('/ask', json={'document_text': 'Test document', 'question': ''})
    assert response.status_code == 400
    assert 'error' in response.json