import pytest
from flask import json

from app.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_chat_page(client):
    """Test the main chat page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Travel Chatbot' in response.data


def test_chat_api_v1_streaming(client, mocker):
    """Test the streaming chat API"""

    # Mock the requests.post to simulate streaming response from the llamafile API
    def mock_stream_response(*args, **kwargs):
        class MockResponse:
            def __init__(self, text):
                self.text = text

            def iter_lines(self):
                for part in self.text.split('\n'):
                    yield part.encode('utf-8')

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        return MockResponse("streaming\nresponse\n")

    # Mock the requests.post call
    mocker.patch('requests.post', side_effect=mock_stream_response)

    conversation = [
        {"role": "user", "content": "Tell me about Paris"},
    ]

    response = client.post('/api/v1/chat', json={'conversation': conversation})
    assert response.status_code == 200
    assert response.mimetype == 'text/event-stream'

    # Collect streamed data
    streamed_data = []
    for chunk in response.response:
        streamed_data.append(chunk.decode('utf-8').strip())

    # Validate the expected streamed content
    assert "streaming" in streamed_data
    assert "response" in streamed_data
