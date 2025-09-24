"""
Serialization utilities for converting between library data structures and API formats.
"""
import json
import base64
from typing import Dict, Any
from dataclasses import asdict

from ..logic.models import GameState, Grid, Mark


class GameStateSerializer:
    """Handles serialization between GameState objects and API-compatible dictionaries."""
    
    @staticmethod
    def to_dict(game_state: GameState) -> Dict[str, Any]:
        """Convert GameState to dictionary format for API."""
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
    
    @staticmethod
    def from_dict(state_dict: Dict[str, Any]) -> GameState:
        """Convert dictionary format back to GameState."""
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
    
    @staticmethod
    def encode(game_state: GameState) -> str:
        """Encode game state to a base64 string."""
        state_dict = GameStateSerializer.to_dict(game_state)
        state_json = json.dumps(state_dict)
        return base64.b64encode(state_json.encode()).decode()
    
    @staticmethod
    def decode(encoded_state: str) -> GameState:
        """Decode base64 string back to game state."""
        try:
            state_json = base64.b64decode(encoded_state.encode()).decode()
            state_dict = json.loads(state_json)
            return GameStateSerializer.from_dict(state_dict)
        except Exception as e:
            raise ValueError(f"Invalid game state encoding: {str(e)}")
