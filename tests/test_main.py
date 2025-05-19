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
    """Test missing email_text returns 400 Bad Request"""
    response = client.post('/summarize', json={})
    assert response.status_code == 400
    assert b'No email text provided' in response.data

def test_summarize_valid_request(client):
    """Test valid request returns summary"""
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Sample summary"))
    ]
    
    with patch('yourapp.client.chat.completions.create', return_value=mock_response) as mock_openai:
        test_email = "This is a test email about important business matters."
        response = client.post('/summarize', json={'email_text': test_email})
        
        assert response.status_code == 200
        assert 'summary' in response.json
        assert response.json['summary'] == "Sample summary"
        mock_openai.assert_called_once()