# backend/main.py - This is the Firebase-generated file, now modified by you
import functions_framework
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse
from starlette.types import Scope, Receive, Send

# Import your actual FastAPI application instance
# Make sure this path is correct if your FastAPI app is named something else, e.g., 'your_fastapi_app_name:app'
from main import app as fastapi_app_instance

# This is a critical step for FastAPI on Cloud Functions:
# We create a wrapper function that Cloud Functions can call,
# and this wrapper will then pass the request to your FastAPI app.
# This pattern is often referred to as a "ASGI wrapper" or "Serverless ASGI Adapter".

@functions_framework.http
async def serve_fastapi(request):
    """
    HTTP Cloud Function that serves your FastAPI application.
    """
    # Cloud Functions (Flask-like) request object is converted to ASGI scope.
    # This is a simplified conversion. For more robust solutions, consider
    # libraries like `asgi-lifespan` or `fastapi-serverless-uvicorn`.
    # For typical use cases, this manual conversion works well.

    # Parse request body (Cloud Functions gives us data directly or via get_json)
    body = request.get_data() # Gets raw bytes
    if request.content_type == 'application/json':
        # FastAPI expects bytes for JSON, so we send raw bytes
        pass
    elif request.content_type and 'text/' in request.content_type:
        # Handle text-based content types if needed
        body = body.decode('utf-8')

    # Build ASGI scope
    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "server": ("localhost", 8080), # Placeholder
        "client": (request.remote_addr, 0) if request.remote_addr else ("127.0.0.1", 0),
        "scheme": request.scheme,
        "method": request.method,
        "root_path": "", # Adjust if your app is mounted on a subpath
        "path": request.path,
        "raw_path": request.path.encode('latin-1'),
        "query_string": request.query_string,
        "headers": [(key.lower().encode('latin-1'), value.encode('latin-1')) for key, value in request.headers.items()],
        "state": {},
        "extensions": {"http.response.template": {}}
    }

    async def receive() -> dict:
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message: dict) -> None:
        nonlocal response_status, response_headers, response_body
        if message["type"] == "http.response.start":
            response_status = message["status"]
            response_headers = [(k.decode(), v.decode()) for k, v in message["headers"]]
        elif message["type"] == "http.response.body":
            response_body += message.get("body", b"")

    response_status = 200
    response_headers = []
    response_body = b""

    # Call the FastAPI application
    await fastapi_app_instance(scope, receive, send)

    # Build Flask-compatible response from collected data
    cf_response = StarletteResponse(
        content=response_body,
        status_code=response_status,
        headers={k: v for k, v in response_headers}
    )
    return cf_response
