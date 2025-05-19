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
    assert b'No email text provided' in response.data
