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
def test_summarize_email_no_payload(mocker):
    with app.test_client() as client:
        mocker.patch('app.OpenAI')  # Assume OpenAI is mocked correctly
        response = client.post('/summarize', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

def test_summarize_email_successful(mocker):
    with app.test_client() as client:
        mocker.patch('app.OpenAI')  # Assume OpenAI is mocked correctly
        mocker.patch('app.request', json={'email_text': 'Email content'})
        response = client.post('/summarize', json={'email_text': 'Email content'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'summary' in data

def test_summarize_email_exception(mocker):
    with app.test_client() as client:
        mocker.patch('app.OpenAI')  # Assume OpenAI is mocked correctly
        mocker.patch('app.request', json={'email_text': 'Email content'})
        mocker.patch('app.client.chat.completions.create', side_effect=Exception('OpenAI Error'))
        response = client.post('/summarize', json={'email_text': 'Email content'})
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

def test_ask_question_no_text(mocker):
    with app.test_client() as client:
        mocker.patch('app.OpenAI')  # Assume OpenAI is mocked correctly
        response = client.post('/ask', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

def test_ask_question_no_question(mocker):
    with app.test_client() as client:
        mocker.patch('app.OpenAI')  # Assume OpenAI is mocked correctly
        response = client.post('/ask', json={'document_text': 'Document content'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

def test_ask_question_successful(mocker):
    with app.test_client() as client:
        mocker.patch('app.OpenAI')  # Assume OpenAI is mocked correctly
        mocker.patch('app.request', json={'document_text': 'Document content', 'question': 'Sample question'})
        response = client.post('/ask', json={'document_text': 'Document content', 'question': 'Sample question'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'answer' in data

def test_ask_question_exception(mocker):
    with app.test_client() as client:
        mocker.patch('app.OpenAI')  # Assume OpenAI is mocked correctly
        mocker.patch('app.request', json={'document_text': 'Document content', 'question': 'Sample question'})
        mocker.patch('app.client.chat.completions.create', side_effect=Exception('OpenAI Error'))
        response = client.post('/ask', json={'document_text': 'Document content', 'question': 'Sample question'})
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data