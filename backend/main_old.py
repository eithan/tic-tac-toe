# Firebase Cloud Functions entry point
import functions_framework
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse
import json
import asyncio

# Import the actual FastAPI app from the server module
from server import app as fastapi_app

@functions_framework.http
def main(request):
    """
    HTTP Cloud Function that serves the FastAPI application.
    This is the entry point for Firebase Cloud Functions.
    """
    # Convert Flask request to ASGI scope
    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "server": ("localhost", 8080),
        "client": (request.remote_addr, 0) if request.remote_addr else ("127.0.0.1", 0),
        "scheme": request.scheme,
        "method": request.method,
        "root_path": "",
        "path": request.path,
        "raw_path": request.path.encode('latin-1'),
        "query_string": request.query_string,
        "headers": [(key.lower().encode('latin-1'), value.encode('latin-1')) for key, value in request.headers.items()],
        "state": {},
        "extensions": {"http.response.template": {}}
    }

    # Get request body
    body = request.get_data()
    if request.content_type == 'application/json':
        try:
            body = json.dumps(request.get_json()).encode('utf-8')
        except:
            body = request.get_data()

    # Response variables
    response_status = 200
    response_headers = []
    response_body = b""

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        nonlocal response_status, response_headers, response_body
        if message["type"] == "http.response.start":
            response_status = message["status"]
            response_headers = [(k.decode(), v.decode()) for k, v in message["headers"]]
        elif message["type"] == "http.response.body":
            response_body += message.get("body", b"")

    # Run the FastAPI app
    async def run_app():
        await fastapi_app(scope, receive, send)

    # Execute the async function
    asyncio.run(run_app())

    # Return the response
    return JSONResponse(
        content=response_body.decode('utf-8') if response_body else "",
        status_code=response_status,
        headers={k: v for k, v in response_headers}
    )