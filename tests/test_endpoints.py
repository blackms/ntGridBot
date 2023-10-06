import httpx
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# Test starting the bot
def test_start_bot():
    config = {
        # Sample configuration for the test
        "trading_pair": "BTC/USDT",
        # ... add other configuration parameters as needed
    }
    response = client.post("/bot/start", json=config)
    assert response.status_code == 200
    assert response.json() == {"status": "Bot started successfully"}


# Test stopping the bot
def test_stop_bot():
    response = client.post("/bot/stop")
    assert response.status_code == 200
    assert response.json() == {"status": "Bot stopped successfully"}


# Test getting bot status
def test_get_bot_status():
    response = client.get("/bot/status")
    assert response.status_code == 200
    assert "status" in response.json()


# Test updating bot configuration
def test_update_config():
    config = {
        # Sample updated configuration for the test
        "trading_pair": "ETH/USDT",
        # ... add other configuration parameters as needed
    }
    response = client.post("/bot/config/update", json=config)
    assert response.status_code == 200
    assert response.json() == {"status": "Configuration updated successfully"}


# Test fetching current configuration
def test_get_config():
    response = client.get("/bot/config")
    assert response.status_code == 200
    assert "config" in response.json()


# Test starting a specific grid instance
def test_start_instance():
    config = {
        # Sample configuration for starting a grid instance
        "trading_pair": "BTC/USDT",
        # ... add other configuration parameters as needed
    }
    response = client.post("/bot/start_instance", json=config)
    assert response.status_code == 200
    assert "status" in response.json()


# Test stopping a specific grid instance
def test_stop_instance():
    # Assuming instance_id 1 for the test. Adjust as needed.
    response = client.post("/bot/stop_instance/1")
    assert response.status_code == 200
    assert "status" in response.json()
