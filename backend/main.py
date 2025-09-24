# backend/main.py - Consolidated Backend with Environment-Based Security
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from tic_tac_toe.game.game_service import GameService

# Environment detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

# Initialize FastAPI app with environment-appropriate settings
app = FastAPI(
    title="Tic-Tac-Toe API",
    description=f"Tic-Tac-Toe game API ({ENVIRONMENT} mode)",
    version="1.0.0"
)

# Security features (only in production or when explicitly enabled)
if IS_PRODUCTION or os.getenv("ENABLE_SECURITY", "false").lower() == "true":
    # Security middleware (no rate limiting for small-scale game)
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
    
    SECURITY_ENABLED = True
    print(f"🔒 Security features enabled ({ENVIRONMENT} mode) - CORS protection only")
else:
    SECURITY_ENABLED = False
    print(f"🚀 Running in development mode (security disabled)")

# Environment-based CORS configuration
def get_allowed_origins():
    """Get CORS origins based on environment"""
    origins = []
    
    if IS_PRODUCTION:
        # Production: Only allow specified origins
        production_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
        origins.extend([origin.strip() for origin in production_origins if origin.strip()])
        if not origins:
            print("⚠️  No ALLOWED_ORIGINS set for production. This may cause CORS issues.")
    else:
        # Development: Allow common development origins
        origins.extend([
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://192.168.1.33:5173",  # Keep existing hardcoded URL
            "https://dialogic-unponderous-melody.ngrok-free.app",  # Keep existing ngrok URL
        ])
    
    return origins

# Configure CORS
cors_config = {
    "allow_origins": get_allowed_origins(),
    "allow_credentials": True,
}

if IS_PRODUCTION:
    # Production: Restrict methods and headers
    cors_config.update({
        "allow_methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"],
    })
else:
    # Development: Allow all methods and headers
    cors_config.update({
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    })

app.add_middleware(CORSMiddleware, **cors_config)

# Initialize game service
game_service = GameService()

# Simple request validation for small-scale game
def validate_request_origin(request: Request):
    """Basic validation to ensure requests come from expected sources"""
    if not IS_PRODUCTION:
        return True  # Skip validation in development
    
    # In production, check if request comes from allowed origins
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    
    allowed_origins = get_allowed_origins()
    
    # Allow if origin or referer matches allowed origins
    if origin and any(origin.startswith(allowed) for allowed in allowed_origins):
        return True
    if referer and any(referer.startswith(allowed) for allowed in allowed_origins):
        return True
    
    # Allow direct API calls (no origin/referer) - for testing
    if not origin and not referer:
        return True
    
    return False

# Rate limiting removed for small-scale game - no decorator needed

# Game endpoints
@app.post("/game_state", tags=["game"])
async def get_game_state(request_data: dict | None = None, request: Request = None):
    """Returns the current game state. If no encoded_state provided, returns initial state."""
    # Validate request origin in production
    if request and not validate_request_origin(request):
        raise HTTPException(status_code=403, detail="Request not allowed from this origin")
    
    try:
        if request_data and "encoded_state" in request_data:
            # Decode the provided game state
            game_state = game_service.decode_game_state(request_data["encoded_state"])
        else:
            # Return initial game state
            game_state = game_service.create_initial_game_state()
        
        return {
            "game_state": game_service.get_game_state_dict(game_state),
            "encoded_state": game_service.encode_game_state(game_state)
        }
    except Exception as e:
        if SECURITY_ENABLED:
            # Log the actual error for debugging but don't expose it
            print(f"Internal error in get_game_state: {e}")
            raise HTTPException(status_code=400, detail="Invalid game state")
        else:
            # Development: Show full error for debugging
            raise HTTPException(status_code=400, detail=str(e))

@app.post("/game_move", tags=["game"])
async def handle_game_move(request_data: dict, request: Request = None):
    """Processes a move and returns the updated game state."""
    # Validate request origin in production
    if request and not validate_request_origin(request):
        raise HTTPException(status_code=403, detail="Request not allowed from this origin")
    
    try:
        # Extract move, game state, and player types from request
        move = request_data.get("move", {})
        encoded_state = request_data.get("encoded_state")
        player_types = request_data.get("player_types", {})
        
        if not encoded_state:
            raise ValueError("No game state provided")
        
        # Decode the current game state
        current_state = game_service.decode_game_state(encoded_state)
        
        # Process the move
        if move and "index" in move:
            # Human move
            updated_state = game_service.make_move(current_state, move["index"])
        else:
            # Computer move - determine which player should move
            current_player = current_state.current_mark.value
            if current_player == "X":
                player_type = player_types.get("x_player_type", "human")
            else:
                player_type = player_types.get("o_player_type", "human")
            
            if player_type == "human":
                raise ValueError("It's a human player's turn, but no move provided")
            
            # Make computer move
            updated_state = game_service.make_computer_move(current_state, player_type)
        
        return {
            "game_state": game_service.get_game_state_dict(updated_state),
            "encoded_state": game_service.encode_game_state(updated_state)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if SECURITY_ENABLED:
            # Log the actual error for debugging but don't expose it
            print(f"Internal error in handle_game_move: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        else:
            # Development: Show full error for debugging
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset_game", tags=["game"])
async def reset_game():
    """Returns a fresh initial game state."""
    try:
        initial_state = game_service.create_initial_game_state()
        return {
            "game_state": game_service.get_game_state_dict(initial_state),
            "encoded_state": game_service.encode_game_state(initial_state)
        }
    except Exception as e:
        if SECURITY_ENABLED:
            print(f"Internal error in reset_game: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/player_types", tags=["game"])
async def get_player_types():
    """Returns available player types."""
    try:
        return {
            "player_types": game_service.get_available_player_types()
        }
    except Exception as e:
        if SECURITY_ENABLED:
            print(f"Internal error in get_player_types: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        else:
            raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint (no rate limiting)
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers."""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "security_enabled": SECURITY_ENABLED
    }

# Entry point for running with uvicorn
if __name__ == "__main__":
    print(f"🚀 Starting Tic-Tac-Toe API in {ENVIRONMENT} mode")
    print(f"🔒 Security features: {'Enabled' if SECURITY_ENABLED else 'Disabled'}")
    print(f"🌐 CORS origins: {get_allowed_origins()}")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)), 
        reload=ENVIRONMENT == "development"
    )