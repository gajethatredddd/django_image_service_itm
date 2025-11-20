def test_api_router_import():
    """Test that API router can be imported"""
    from app.api.router import api_router
    assert api_router is not None
    assert len(api_router.routes) > 0

def test_health_router_import():
    """Test that health router can be imported"""
    from app.api.routes.health import router as health_router
    assert health_router is not None

def test_emails_router_import():
    """Test that emails router can be imported"""
    from app.api.routes.emails import router as emails_router
    assert emails_router is not None