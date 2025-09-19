# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import base64

from tic_tac_toe.logic.models import GameState, Grid, Mark
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.game.players import RandomComputerPlayer, MinimaxComputerPlayer

# Import neuralnet players - add path if needed
import sys
from pathlib import Path
neuralnet_path = Path(__file__).parent.parent / "neuralnet"
if str(neuralnet_path) not in sys.path:
    sys.path.insert(0, str(neuralnet_path))

from models.players import AlphaZeroStatelessComputerPlayer

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

def get_initial_game_state():
    """Creates a new game state using the library."""
    return GameState(Grid(), Mark("X"))

def game_state_to_dict(game_state: GameState):
    """Converts GameState to dictionary format for API."""
    # Convert the grid cells to a list format expected by frontend
    board = ["" if cell == " " else cell for cell in game_state.grid.cells]
    
    # Determine game status and message
    if game_state.game_over:
        status = "finished"
        if game_state.winner:
            message = f"Player {game_state.winner.value} wins!"
            current_player = game_state.winner.value
        else:
            message = "It's a draw!"
            current_player = game_state.current_mark.value
    else:
        status = "in_progress"
        message = f"Player {game_state.current_mark.value}'s turn"
        current_player = game_state.current_mark.value
    
    return {
        "board": board,
        "current_player": current_player,
        "status": status,
        "message": message,
    }

def dict_to_game_state(state_dict: dict):
    """Converts dictionary format back to GameState."""
    # Convert board list to grid string
    grid_cells = "".join(" " if cell == "" else cell for cell in state_dict["board"])
    
    grid = Grid(grid_cells)
    
    # Determine starting mark based on the board state
    if grid.x_count > grid.o_count:
        starting_mark = Mark("X")
    elif grid.o_count > grid.x_count:
        starting_mark = Mark("O")
    else:
        starting_mark = Mark(state_dict.get("current_player", "X"))
    
    return GameState(grid, starting_mark)

def make_move(game_state: GameState, move: dict):
    """Updates the game state based on a player's move using the library."""
    index = move.get("index")
    
    if game_state.game_over:
        raise ValueError("Game is already over.")
    if index is None or not 0 <= index < 9:
        raise ValueError("Invalid move index.")
    
    try:
        # Use the library's make_move_to method
        move_obj = game_state.make_move_to(index)
        return move_obj.after_state
    except InvalidMove as e:
        raise ValueError(str(e))

def make_computer_move(game_state: GameState, player_type: str):
    """Makes a computer move based on the player type."""
    current_mark = game_state.current_mark
    
    # Check if game is already over
    if game_state.game_over:
        raise ValueError("Cannot make move: game is already over")
    
    if player_type == "random":
        computer_player = RandomComputerPlayer(current_mark, delay_seconds=0)
        return computer_player.make_move(game_state)
    elif player_type == "minimax":
        computer_player = MinimaxComputerPlayer(current_mark, delay_seconds=0)
        return computer_player.make_move(game_state)
    elif player_type == "alphazero":
        computer_player = AlphaZeroStatelessComputerPlayer(current_mark)
        return computer_player.make_move(game_state)
    else:
        raise ValueError(f"Unknown computer player type: {player_type}")

def encode_game_state(game_state: GameState):
    """Encodes game state to a base64 string."""
    state_dict = game_state_to_dict(game_state)
    state_json = json.dumps(state_dict)
    return base64.b64encode(state_json.encode()).decode()

def decode_game_state(encoded_state):
    """Decodes base64 string back to game state."""
    try:
        state_json = base64.b64decode(encoded_state.encode()).decode()
        state_dict = json.loads(state_json)
        return dict_to_game_state(state_dict)
    except Exception as e:
        raise ValueError(f"Invalid game state encoding: {str(e)}")

@app.post("/game_state", tags=["game"])
async def get_game_state(request: dict | None = None):
    """Returns the current game state. If no encoded_state provided, returns initial state."""
    try:
        if request and "encoded_state" in request:
            # Decode the provided game state
            game_state = decode_game_state(request["encoded_state"])
        else:
            # Return initial game state
            game_state = get_initial_game_state()
        
        return {
            "game_state": game_state_to_dict(game_state),
            "encoded_state": encode_game_state(game_state)
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
        current_state = decode_game_state(encoded_state)
        
        # Process the move
        if move and "index" in move:
            # Human move
            updated_state = make_move(current_state, move)
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
            updated_state = make_computer_move(current_state, player_type)
        
        return {
            "game_state": game_state_to_dict(updated_state),
            "encoded_state": encode_game_state(updated_state)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reset_game", tags=["game"])
async def reset_game():
    """Returns a fresh initial game state."""
    initial_state = get_initial_game_state()
    return {
        "game_state": game_state_to_dict(initial_state),
        "encoded_state": encode_game_state(initial_state)
    }

# Entry point for running with uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

