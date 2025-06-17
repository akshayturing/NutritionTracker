import json
import pytest

def test_api_docs_endpoint(client):
    """Test getting API documentation."""
    response = client.get('/api/docs/')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'api_name' in data
    assert 'version' in data
    assert 'endpoints' in data
    assert len(data['endpoints']) > 0