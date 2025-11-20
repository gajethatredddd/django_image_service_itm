def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data

def test_root_redirect(client):
    """Test root redirect to form"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect

def test_openapi_docs(client):
    """Test OpenAPI docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_json(client):
    """Test OpenAPI JSON schema"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data