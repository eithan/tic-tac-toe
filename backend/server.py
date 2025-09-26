# backend/server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from tic_tac_toe.game.game_service import GameService

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # React development server
    "http://192.168.1.33:5173", # Hard-coded url to React development server for phone to work
    "https://dialogic-unponderous-melody.ngrok-free.app",  # ngrok URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game service
game_service = GameService()

# All conversion and game logic functions have been moved to GameService

@app.post("/game_state", tags=["game"])
async def get_game_state(request: dict | None = None):
    """Returns the current game state. If no encoded_state provided, returns initial state."""
    try:
        if request and "encoded_state" in request:
            # Decode the provided game state
            game_state = game_service.decode_game_state(request["encoded_state"])
        else:
            # Return initial game state
            game_state = game_service.create_initial_game_state()
        
        return {
            "game_state": game_service.get_game_state_dict(game_state),
            "encoded_state": game_service.encode_game_state(game_state)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/game_move", tags=["game"])
async def handle_game_move(request: dict):
    """Processes a move and returns the updated game state."""
    try:
        # Extract move, game state, and player types from request
        move = request.get("move", {})
        encoded_state = request.get("encoded_state")
        player_types = request.get("player_types", {})
        
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


@app.post("/reset_game", tags=["game"])
async def reset_game():
    """Returns a fresh initial game state."""
    initial_state = game_service.create_initial_game_state()
    return {
        "game_state": game_service.get_game_state_dict(initial_state),
        "encoded_state": game_service.encode_game_state(initial_state)
    }

@app.get("/player_types", tags=["game"])
async def get_player_types():
    """Returns available player types."""
    return {
        "player_types": game_service.get_available_player_types()
    }

# Entry point for running with uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

