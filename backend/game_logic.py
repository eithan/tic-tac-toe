"""
Simplified game logic for Cloud Run deployment.
Includes basic game functionality without neural network dependencies.
"""
import base64
import json
from typing import Dict, Any, List, Optional
from enum import Enum

class Mark(Enum):
    """Player marks."""
    X = "X"
    O = "O"
    EMPTY = ""

class Grid:
    """3x3 grid for tic-tac-toe."""
    
    def __init__(self):
        self.cells = [Mark.EMPTY] * 9
    
    def get_cell(self, index: int) -> Mark:
        """Get cell value by index."""
        if 0 <= index < 9:
            return self.cells[index]
        return Mark.EMPTY
    
    def set_cell(self, index: int, mark: Mark) -> bool:
        """Set cell value by index. Returns True if successful."""
        if 0 <= index < 9 and self.cells[index] == Mark.EMPTY:
            self.cells[index] = mark
            return True
        return False
    
    def force_set_cell(self, index: int, mark: Mark) -> None:
        """Force set cell value by index (for minimax algorithm)."""
        if 0 <= index < 9:
            self.cells[index] = mark
    
    def is_full(self) -> bool:
        """Check if grid is full."""
        return all(cell != Mark.EMPTY for cell in self.cells)
    
    def get_winning_cells(self) -> Optional[List[int]]:
        """Get winning cells if there's a winner."""
        # Check rows
        for i in range(0, 9, 3):
            if (self.cells[i] != Mark.EMPTY and 
                self.cells[i] == self.cells[i+1] == self.cells[i+2]):
                return [i, i+1, i+2]
        
        # Check columns
        for i in range(3):
            if (self.cells[i] != Mark.EMPTY and 
                self.cells[i] == self.cells[i+3] == self.cells[i+6]):
                return [i, i+3, i+6]
        
        # Check diagonals
        if (self.cells[0] != Mark.EMPTY and 
            self.cells[0] == self.cells[4] == self.cells[8]):
            return [0, 4, 8]
        
        if (self.cells[2] != Mark.EMPTY and 
            self.cells[2] == self.cells[4] == self.cells[6]):
            return [2, 4, 6]
        
        return None

class GameState:
    """Game state representation."""
    
    def __init__(self, grid: Grid, current_mark: Mark):
        self.grid = grid
        self.current_mark = current_mark
        self.game_over = False
        self.winner = None
        self.winning_cells = None
        
        # Check for game end
        winning_cells = grid.get_winning_cells()
        if winning_cells:
            self.game_over = True
            self.winner = grid.get_cell(winning_cells[0])
            self.winning_cells = winning_cells
        elif grid.is_full():
            self.game_over = True
            self.winner = Mark.EMPTY  # Draw

class GameService:
    """Service for managing game logic."""
    
    def __init__(self):
        self.available_player_types = ["human", "random", "minimax"]
    
    def create_initial_game_state(self) -> GameState:
        """Create a new initial game state."""
        return GameState(Grid(), Mark.X)
    
    def make_move(self, game_state: GameState, index: int) -> GameState:
        """Make a move on the board."""
        if game_state.game_over:
            raise ValueError("Game is already over")
        
        if not game_state.grid.set_cell(index, game_state.current_mark):
            raise ValueError("Invalid move")
        
        # Switch player
        next_mark = Mark.O if game_state.current_mark == Mark.X else Mark.X
        
        return GameState(game_state.grid, next_mark)
    
    def make_computer_move(self, game_state: GameState, player_type: str) -> GameState:
        """Make a computer move."""
        if player_type == "random":
            return self._make_random_move(game_state)
        elif player_type == "minimax":
            return self._make_minimax_move(game_state)
        else:
            raise ValueError(f"Unknown player type: {player_type}")
    
    def _make_random_move(self, game_state: GameState) -> GameState:
        """Make a random move."""
        import random
        empty_cells = [i for i in range(9) if game_state.grid.get_cell(i) == Mark.EMPTY]
        if not empty_cells:
            raise ValueError("No empty cells available")
        
        move = random.choice(empty_cells)
        return self.make_move(game_state, move)
    
    def _make_minimax_move(self, game_state: GameState) -> GameState:
        """Make a minimax move."""
        best_score, best_move = self._minimax(game_state.grid, game_state.current_mark, True)
        if best_move is None:
            # Fallback to random move if minimax fails
            return self._make_random_move(game_state)
        return self.make_move(game_state, best_move)
    
    def _minimax(self, grid: Grid, player: Mark, is_maximizing: bool) -> tuple:
        """Minimax algorithm for optimal moves."""
        # Check terminal states
        winning_cells = grid.get_winning_cells()
        if winning_cells:
            winner = grid.get_cell(winning_cells[0])
            if winner == player:
                return 1, None
            else:
                return -1, None
        
        if grid.is_full():
            return 0, None
        
        # Get available moves
        empty_cells = [i for i in range(9) if grid.get_cell(i) == Mark.EMPTY]
        
        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for move in empty_cells:
                # Make move
                grid.force_set_cell(move, player)
                score, _ = self._minimax(grid, Mark.O if player == Mark.X else Mark.X, False)
                # Undo move
                grid.force_set_cell(move, Mark.EMPTY)
                
                if score > best_score:
                    best_score = score
                    best_move = move
            
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in empty_cells:
                # Make move
                grid.force_set_cell(move, player)
                score, _ = self._minimax(grid, Mark.O if player == Mark.X else Mark.X, True)
                # Undo move
                grid.force_set_cell(move, Mark.EMPTY)
                
                if score < best_score:
                    best_score = score
                    best_move = move
            
            return best_score, best_move
    
    def get_game_state_dict(self, game_state: GameState) -> Dict[str, Any]:
        """Convert game state to dictionary."""
        board = [cell.value for cell in game_state.grid.cells]
        current_player = game_state.current_mark.value
        
        if game_state.game_over:
            if game_state.winner == Mark.EMPTY:
                status = "draw"
                message = "It's a draw!"
            else:
                status = "finished"
                message = f"Player {game_state.winner.value} wins!"
        else:
            status = "in_progress"
            message = f"Player {current_player}'s turn"
        
        result = {
            "board": board,
            "current_player": current_player,
            "status": status,
            "message": message,
        }
        
        if game_state.game_over and game_state.winner and game_state.winning_cells:
            result["winning_cells"] = game_state.winning_cells
        
        return result
    
    def encode_game_state(self, game_state: GameState) -> str:
        """Encode game state to base64 string."""
        state_dict = self.get_game_state_dict(game_state)
        json_str = json.dumps(state_dict)
        return base64.b64encode(json_str.encode()).decode()
    
    def decode_game_state(self, encoded_state: str) -> GameState:
        """Decode base64 string to game state."""
        try:
            json_str = base64.b64decode(encoded_state.encode()).decode()
            state_dict = json.loads(json_str)
            
            # Reconstruct grid
            grid = Grid()
            for i, cell_value in enumerate(state_dict["board"]):
                if cell_value:
                    grid.set_cell(i, Mark(cell_value))
            
            # Reconstruct game state
            current_mark = Mark(state_dict["current_player"])
            game_state = GameState(grid, current_mark)
            
            return game_state
        except Exception as e:
            raise ValueError(f"Invalid game state: {e}")
    
    def get_available_player_types(self) -> List[str]:
        """Get list of available player types."""
        return self.available_player_types
