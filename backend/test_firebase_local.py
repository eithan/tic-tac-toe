#!/usr/bin/env python3
"""
Test Firebase function locally
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

def test_firebase_function():
    print("🧪 Testing Firebase Cloud Function locally...")
    
    try:
        from main import serve_fastapi_function
        
        # Test health endpoint
        request = MockRequest(method="GET", path="/health")
        response = serve_fastapi_function(request)
        
        print(f"✅ Health check response: {response.status_code}")
        print(f"📄 Response body: {response.body}")
        
        print("🎉 Firebase function test passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_firebase_function()
