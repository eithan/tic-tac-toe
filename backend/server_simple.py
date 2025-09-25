# Simple FastAPI application for testing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Environment detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Initialize FastAPI app
app = FastAPI(
    title="Tic-Tac-Toe API",
    description=f"Tic-Tac-Toe game API ({ENVIRONMENT} mode)",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "message": "Tic-Tac-Toe API is running!"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Tic-Tac-Toe API!"}

# Entry point for running with uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "server_simple:app", 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8080)), 
        reload=ENVIRONMENT == "development"
    )
