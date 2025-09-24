"""
Game service that handles game logic and player management.
Separates game logic from API concerns.
"""
from typing import Dict, Any, Optional
from ..logic.models import GameState, Grid, Mark
from ..logic.exceptions import InvalidMove
from .player_factory import PlayerFactory
from ..api.serializers import GameStateSerializer


class GameService:
    """Service class that handles game logic and player management."""
    
    def __init__(self):
        self.player_factory = PlayerFactory()
    
    def create_initial_game_state(self) -> GameState:
        """Create a new initial game state."""
        return GameState(Grid(), Mark("X"))
    
    def make_move(self, game_state: GameState, move_index: int) -> GameState:
        """Make a move on the game state."""
        if game_state.game_over:
            raise ValueError("Game is already over.")
        if not 0 <= move_index < 9:
            raise ValueError("Invalid move index.")
        
        try:
            move_obj = game_state.make_move_to(move_index)
            return move_obj.after_state
        except InvalidMove as e:
            raise ValueError(str(e))
    
    def make_computer_move(self, game_state: GameState, player_type: str) -> GameState:
        """Make a computer move based on the player type."""
        if game_state.game_over:
            raise ValueError("Cannot make move: game is already over")
        
        if not self.player_factory.is_computer_player(player_type):
            raise ValueError(f"Player type '{player_type}' is not a computer player")
        
        # Create a temporary player instance to make the move
        player = self.player_factory.create_player(player_type, game_state.current_mark)
        move = player.get_move(game_state)
        
        if move is None:
            raise ValueError("Computer player failed to make a move")
        
        return move.after_state
    
    def get_game_state_dict(self, game_state: GameState) -> Dict[str, Any]:
        """Get game state as dictionary for API response."""
        return GameStateSerializer.to_dict(game_state)
    
    def encode_game_state(self, game_state: GameState) -> str:
        """Encode game state to base64 string."""
        return GameStateSerializer.encode(game_state)
    
    def decode_game_state(self, encoded_state: str) -> GameState:
        """Decode base64 string to game state."""
        return GameStateSerializer.decode(encoded_state)
    
    def get_available_player_types(self) -> list[str]:
        """Get list of available player types."""
        return self.player_factory.get_available_types()
