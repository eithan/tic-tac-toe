# backend/firebase_main.py (or functions/main.py - adjust path as needed)
import os
from firebase_functions.https import onRequest # Use Firebase's onRequest decorator
from firebase_admin import initialize_app # For initializing Firebase Admin SDK
from starlette.middleware.wsgi import WSGIMiddleware # To adapt FastAPI to WSGI environment

# IMPORTANT: Initialize Firebase Admin SDK FIRST.
# This should happen once globally for your function.
initialize_app()

# Import your actual FastAPI application instance.
# Ensure this import path is correct relative to where firebase_main.py is located.
# If firebase_main.py is in 'functions' and main.py is in 'backend', you might need
# a relative import like 'from .main import app' if 'backend' is treated as a package,
# or adjust your project structure/deployment configuration.
# For simplicity, let's assume 'main.py' is importable directly if it's in a sibling directory
# or if 'backend' is the root of your functions code.
from server import app as fastapi_app_instance

# Wrap your FastAPI app with WSGIMiddleware.
# This makes your ASGI (FastAPI) application compatible with the WSGI-like
# request object that Firebase's onRequest decorator provides.
wsgi_app = WSGIMiddleware(fastapi_app_instance)

# Define your Firebase HTTP Cloud Function using the Firebase SDK decorator
@onRequest(region="us-central1", timeout_sec=60) # Adjust region and timeout as needed
def serve_fastapi_function(request):
    """
    HTTP Firebase Cloud Function that serves your FastAPI application.
    """
    # The 'request' object here is a Flask-like request.
    # The WSGIMiddleware handles the conversion to an ASGI scope for FastAPI.
    return wsgi_app(request)

# Optional: You can keep your uvicorn __main__ block in main.py for local development,
# but it won't be used by Firebase Cloud Functions.
