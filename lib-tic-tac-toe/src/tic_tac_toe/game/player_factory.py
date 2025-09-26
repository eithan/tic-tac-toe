"""
Factory for creating player instances based on type strings.
Unifies player creation across different frontends.
"""
from typing import Dict, Type, Optional
from ..logic.models import Mark
from .players import Player, RandomComputerPlayer, MinimaxComputerPlayer

# Import neuralnet players with error handling
try:
    from neuralnet.models.players import AlphaZeroStatelessComputerPlayer
    NEURALNET_AVAILABLE = True
except ImportError as e:
    print(f"Error importing AlphaZeroStatelessComputerPlayer: {e}")
    NEURALNET_AVAILABLE = False
    AlphaZeroStatelessComputerPlayer = None


class PlayerFactory:
    """Factory for creating player instances based on type strings."""
    
    # Registry of available player types
    _player_types: Dict[str, Type[Player]] = {
        "random": RandomComputerPlayer,
        "minimax": MinimaxComputerPlayer,
    }
    
    @classmethod
    def register_player_type(cls, player_type: str, player_class: Type[Player]) -> None:
        """Register a new player type."""
        cls._player_types[player_type] = player_class
    
    @classmethod
    def get_available_types(cls) -> list[str]:
        """Get list of available player types."""
        types = list(cls._player_types.keys())
        if NEURALNET_AVAILABLE:
            types.append("alphazero")
        return types
    
    @classmethod
    def create_player(cls, player_type: str, mark: Mark) -> Player:
        """Create a player instance of the specified type."""
        if player_type == "alphazero":
            if not NEURALNET_AVAILABLE:
                raise ValueError("AlphaZero player not available - neuralnet module not found")
            return AlphaZeroStatelessComputerPlayer(mark)
        
        if player_type not in cls._player_types:
            available = ", ".join(cls.get_available_types())
            raise ValueError(f"Unknown player type: {player_type}. Available types: {available}")
        
        player_class = cls._player_types[player_type]
        return player_class(mark)
    
    @classmethod
    def is_computer_player(cls, player_type: str) -> bool:
        """Check if a player type is a computer player."""
        return player_type in cls.get_available_types() and player_type != "human"
