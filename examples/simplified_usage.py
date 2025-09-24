"""
Example demonstrating the simplified API usage.
This shows how the new abstractions make the code much cleaner.
"""
from tic_tac_toe.game.game_service import GameService
from tic_tac_toe.logic.models import Mark


def main():
    """Demonstrate simplified game service usage."""
    # Create game service
    game_service = GameService()
    
    # Create initial game state
    game_state = game_service.create_initial_game_state()
    print(f"Initial state: {game_service.get_game_state_dict(game_state)}")
    
    # Make a human move
    game_state = game_service.make_move(game_state, 0)  # Top-left corner
    print(f"After human move: {game_service.get_game_state_dict(game_state)}")
    
    # Make a computer move
    game_state = game_service.make_computer_move(game_state, "random")
    print(f"After computer move: {game_service.get_game_state_dict(game_state)}")
    
    # Encode/Decode state
    encoded = game_service.encode_game_state(game_state)
    print(f"Encoded state: {encoded[:50]}...")
    
    decoded = game_service.decode_game_state(encoded)
    print(f"Decoded state matches: {decoded == game_state}")
    
    # Show available player types
    print(f"Available player types: {game_service.get_available_player_types()}")


if __name__ == "__main__":
    main()
