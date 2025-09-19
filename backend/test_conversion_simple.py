#!/usr/bin/env python3
"""Simple unit tests for game_state_to_dict and dict_to_game_state conversion functions."""

import sys
import os
import unittest

# Add the library to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'library', 'src'))

from tic_tac_toe.logic.models import GameState, Grid, Mark

# Import the conversion functions from main.py
sys.path.append(os.path.dirname(__file__))
from main import game_state_to_dict, dict_to_game_state


class TestGameStateConversion(unittest.TestCase):
    """Test cases for GameState conversion functions."""

    def test_empty_game_state_conversion(self):
        """Test conversion of an empty game state."""
        # Create empty game state
        empty_state = GameState(Grid(), Mark("X"))
        
        # Convert to dict
        state_dict = game_state_to_dict(empty_state)
        
        # Verify dict structure
        self.assertEqual(state_dict["board"], ["", "", "", "", "", "", "", "", ""])
        self.assertEqual(state_dict["current_player"], "X")
        self.assertEqual(state_dict["status"], "in_progress")
        self.assertEqual(state_dict["message"], "Player X's turn")
        
        # Convert back to GameState
        converted_state = dict_to_game_state(state_dict)
        
        # Verify all properties match
        self.assertEqual(converted_state.grid.cells, empty_state.grid.cells)
        self.assertEqual(converted_state.starting_mark, empty_state.starting_mark)
        self.assertEqual(converted_state.current_mark, empty_state.current_mark)
        self.assertEqual(converted_state.game_not_started, empty_state.game_not_started)
        self.assertEqual(converted_state.game_over, empty_state.game_over)
        self.assertEqual(converted_state.tie, empty_state.tie)
        self.assertEqual(converted_state.winner, empty_state.winner)
        self.assertEqual(converted_state.winning_cells, empty_state.winning_cells)

    def test_single_move_conversion(self):
        """Test conversion with a single move."""
        # Create game state with one move (X starts)
        grid = Grid("X        ")
        game_state = GameState(grid, Mark("X"))
        
        # Convert to dict
        state_dict = game_state_to_dict(game_state)
        
        # Verify dict structure
        self.assertEqual(state_dict["board"], ["X", "", "", "", "", "", "", "", ""])
        self.assertEqual(state_dict["current_player"], "O")
        self.assertEqual(state_dict["status"], "in_progress")
        self.assertEqual(state_dict["message"], "Player O's turn")
        
        # Convert back to GameState
        converted_state = dict_to_game_state(state_dict)
        
        # Verify all properties match
        self.assertEqual(converted_state.grid.cells, game_state.grid.cells)
        self.assertEqual(converted_state.starting_mark, game_state.starting_mark)
        self.assertEqual(converted_state.current_mark, game_state.current_mark)
        self.assertEqual(converted_state.game_not_started, game_state.game_not_started)
        self.assertEqual(converted_state.game_over, game_state.game_over)
        self.assertEqual(converted_state.tie, game_state.tie)
        self.assertEqual(converted_state.winner, game_state.winner)

    def test_winning_game_state_conversion(self):
        """Test conversion of a winning game state."""
        # Create winning game state (X wins in top row)
        grid = Grid("XXXOO    ")
        game_state = GameState(grid, Mark("X"))
        
        # Convert to dict
        state_dict = game_state_to_dict(game_state)
        
        # Verify dict structure
        self.assertEqual(state_dict["board"], ["X", "X", "X", "O", "O", "", "", "", ""])
        self.assertEqual(state_dict["current_player"], "X")  # Winner is X
        self.assertEqual(state_dict["status"], "finished")
        self.assertEqual(state_dict["message"], "Player X wins!")
        
        # Convert back to GameState
        converted_state = dict_to_game_state(state_dict)
        
        # Verify all properties match
        self.assertEqual(converted_state.grid.cells, game_state.grid.cells)
        self.assertEqual(converted_state.starting_mark, game_state.starting_mark)
        self.assertEqual(converted_state.current_mark, game_state.current_mark)
        self.assertEqual(converted_state.game_not_started, game_state.game_not_started)
        self.assertEqual(converted_state.game_over, game_state.game_over)
        self.assertEqual(converted_state.tie, game_state.tie)
        self.assertEqual(converted_state.winner, game_state.winner)
        self.assertEqual(converted_state.winning_cells, game_state.winning_cells)

    def test_tie_game_state_conversion(self):
        """Test conversion of a tie game state."""
        # Create tie game state (equal number of X and O)
        grid = Grid("XOXOOXXXO")
        game_state = GameState(grid, Mark("X"))
        
        # Convert to dict
        state_dict = game_state_to_dict(game_state)
        
        # Verify dict structure
        self.assertEqual(state_dict["board"], ["X", "O", "X", "O", "O", "X", "X", "X", "O"])
        #self.assertEqual(state_dict["current_player"], "X")  # Starting mark
        self.assertEqual(state_dict["status"], "finished")
        self.assertEqual(state_dict["message"], "It's a draw!")
        
        # Convert back to GameState
        converted_state = dict_to_game_state(state_dict)
        
        # Verify all properties match
        self.assertEqual(converted_state.grid.cells, game_state.grid.cells)
        self.assertEqual(converted_state.starting_mark, game_state.starting_mark)
        self.assertEqual(converted_state.current_mark, game_state.current_mark)
        self.assertEqual(converted_state.game_not_started, game_state.game_not_started)
        self.assertEqual(converted_state.game_over, game_state.game_over)
        self.assertEqual(converted_state.tie, game_state.tie)
        self.assertEqual(converted_state.winner, game_state.winner)

    def test_round_trip_conversion(self):
        """Test that round-trip conversions preserve all data."""
        # Create a game state
        grid = Grid("XOXO X   ")
        original_state = GameState(grid, Mark("X"))
        
        # Perform round-trip conversion
        state_dict = game_state_to_dict(original_state)
        converted_state = dict_to_game_state(state_dict)
        
        # Verify all properties are preserved
        self.assertEqual(converted_state.grid.cells, original_state.grid.cells)
        self.assertEqual(converted_state.starting_mark, original_state.starting_mark)
        self.assertEqual(converted_state.current_mark, original_state.current_mark)
        self.assertEqual(converted_state.game_not_started, original_state.game_not_started)
        self.assertEqual(converted_state.game_over, original_state.game_over)
        self.assertEqual(converted_state.tie, original_state.tie)
        self.assertEqual(converted_state.winner, original_state.winner)
        self.assertEqual(converted_state.winning_cells, original_state.winning_cells)

    def test_grid_properties_preservation(self):
        """Test that Grid properties are correctly preserved."""
        grid = Grid("XOXO X   ")
        game_state = GameState(grid, Mark("X"))
        
        # Get original grid properties
        original_x_count = game_state.grid.x_count
        original_o_count = game_state.grid.o_count
        original_empty_count = game_state.grid.empty_count
        
        # Convert and convert back
        state_dict = game_state_to_dict(game_state)
        converted_state = dict_to_game_state(state_dict)
        
        # Verify grid properties are preserved
        self.assertEqual(converted_state.grid.x_count, original_x_count)
        self.assertEqual(converted_state.grid.o_count, original_o_count)
        self.assertEqual(converted_state.grid.empty_count, original_empty_count)

    def test_possible_moves_preservation(self):
        """Test that possible moves are correctly calculated after conversion."""
        # Create a game state with some moves
        grid = Grid("X O      ")
        game_state = GameState(grid, Mark("X"))
        
        # Get original possible moves
        original_moves = game_state.possible_moves
        original_move_indices = [move.cell_index for move in original_moves]
        
        # Convert and convert back
        state_dict = game_state_to_dict(game_state)
        converted_state = dict_to_game_state(state_dict)
        
        # Get converted possible moves
        converted_moves = converted_state.possible_moves
        converted_move_indices = [move.cell_index for move in converted_moves]
        
        # Verify possible moves are the same
        self.assertEqual(set(original_move_indices), set(converted_move_indices))

    def test_different_starting_marks(self):
        """Test conversion with different starting marks."""
        # Test with O as starting mark (O has one more move)
        grid = Grid("X O      ")
        game_state = GameState(grid, Mark("O"))
        
        # Convert to dict
        state_dict = game_state_to_dict(game_state)
        
        # Verify current player is correct (O's turn since X count == O count)
        self.assertEqual(state_dict["current_player"], "O")
        
        # Convert back to GameState
        converted_state = dict_to_game_state(state_dict)
        
        # Verify starting mark is preserved
        self.assertEqual(converted_state.starting_mark, Mark("O"))
        self.assertEqual(converted_state.current_mark, game_state.current_mark)

    def test_invalid_dict_handling(self):
        """Test handling of invalid dictionary data."""
        # Test with missing board field
        invalid_dict = {"current_player": "X"}
        
        with self.assertRaises(KeyError):
            dict_to_game_state(invalid_dict)
        
        # Test with invalid board length
        invalid_dict = {"board": ["X", "O"], "current_player": "X"}
        
        with self.assertRaises(ValueError):
            dict_to_game_state(invalid_dict)
        
        # Test with invalid current_player
        invalid_dict = {"board": ["", "", "", "", "", "", "", "", ""], "current_player": "Z"}
        
        with self.assertRaises(ValueError):
            dict_to_game_state(invalid_dict)

    def test_state_consistency(self):
        """Test that converted states maintain logical consistency."""
        # Test that game_not_started is correctly preserved
        empty_state = GameState(Grid(), Mark("X"))
        state_dict = game_state_to_dict(empty_state)
        converted_state = dict_to_game_state(state_dict)
        
        self.assertTrue(converted_state.game_not_started)
        self.assertFalse(converted_state.game_over)
        self.assertIsNone(converted_state.winner)
        self.assertFalse(converted_state.tie)
        
        # Test that finished states are correctly identified
        winning_state = GameState(Grid("XXXOO    "), Mark("X"))
        state_dict = game_state_to_dict(winning_state)
        converted_state = dict_to_game_state(state_dict)
        
        self.assertFalse(converted_state.game_not_started)
        self.assertTrue(converted_state.game_over)
        self.assertIsNotNone(converted_state.winner)
        self.assertFalse(converted_state.tie)


if __name__ == "__main__":
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGameStateConversion)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
