#!/usr/bin/env python3
"""
Test script for Firebase Cloud Functions
"""
import json
from unittest.mock import Mock

# Mock request object
class MockRequest:
    def __init__(self, method="GET", path="/health", headers=None, data=None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.content_type = "application/json"
        self.remote_addr = "127.0.0.1"
        self.scheme = "http"
        self.query_string = b""
        self._data = data or b"{}"
    
    def get_data(self):
        return self._data
    
    def get_json(self):
        return json.loads(self._data.decode('utf-8'))

# Test the Firebase function
def test_firebase_function():
    print("🧪 Testing Firebase Cloud Function...")
    
    try:
        from main import main
        
        # Test health endpoint
        request = MockRequest(method="GET", path="/health")
        response = main(request)
        
        print(f"✅ Health check response: {response.status_code}")
        print(f"📄 Response body: {response.body}")
        
        # Test game state endpoint
        request = MockRequest(
            method="POST", 
            path="/game_state",
            data=json.dumps({}).encode('utf-8')
        )
        response = main(request)
        
        print(f"✅ Game state response: {response.status_code}")
        print(f"📄 Response body: {response.body[:100]}...")
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_firebase_function()
