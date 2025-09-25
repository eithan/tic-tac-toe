import numpy as np
import pyspiel
from codetiming import Timer
from open_spiel.python.algorithms import mcts
from itertools import zip_longest

from open_spiel.python.algorithms.alpha_zero import evaluator as az_evaluator

from .alphazeromodel import AlphaZeroModel
from tic_tac_toe.game.players import ComputerPlayer
from tic_tac_toe.logic.models import GameState, Move, Mark

import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


def _create_mcts_bot(game, evaluator):
    """Helper function to create MCTS bot with consistent parameters."""
    return mcts.MCTSBot(
        game,
        2,
        50,  # TODO what is optimal here? they had 10000 but it takes much longer to play
        evaluator,
        random_state=np.random.RandomState(),
        child_selection_fn=mcts.SearchNode.puct_value,
        solve=True,
        verbose=False)


# AlphaZeroComputerPlayer removed - use AlphaZeroStatelessComputerPlayer instead

class AlphaZeroStatelessComputerPlayer(ComputerPlayer):
    @Timer(text="AZS.init took {:0.4f} seconds")
    def __init__(self, mark: Mark):
        """
        Creates an Alpha Zero computer player in the format required by our actual game.
        Loading the model takes a little bit of time.

        Loads the trained model from a file distributed with this application.
        Holds its own game state for syncing with our actual game.
        """
        logger.debug(f"AlphaZeroStatelessComputerPlayer.__init__ mark {mark}")
        super().__init__(mark)

    @staticmethod
    def combine_moves(game_state: GameState):
        """
        Alpha Zero needs to play moves alternating between X and O. This method combines the moves into a list of tuples of (mark, index).
        It doesn't matter which mark is first, but it's important to alternate between them as we apply them to the game state.
        """
        x_indexes = [i for i, cell in enumerate(game_state.grid.cells) if cell == "X"]
        o_indexes = [i for i, cell in enumerate(game_state.grid.cells) if cell == "O"]
        
        return [(mark, index) for x_idx, o_idx in zip_longest(x_indexes, o_indexes) 
                for mark, index in [('X', x_idx), ('O', o_idx)] if index is not None]

    def get_computer_move(self, game_state: GameState) -> Move | None:
        """
        Alpha Zero computes its next Tic-Tac-Toe move

        First we create a history of moves from the game state.
        Next we sync Alpha Zero with this history of moves (it's important to play moves alternating between X and O).
        Then we compute our move.
        Finally we convert our move to the actual game representation and return it.
        """
        game = pyspiel.load_game("tic_tac_toe")
        evaluator = az_evaluator.AlphaZeroEvaluator(game, AlphaZeroModel())
        
        with Timer(text="AZS syncing state took {:0.4f} seconds"):
            az_state = game.new_initial_state()
            bot = _create_mcts_bot(game, evaluator)

            for mark, index in AlphaZeroStatelessComputerPlayer.combine_moves(game_state):
                logger.debug(f"Position {index} for '{mark}'")
                logger.debug(f"Applying move {index} to alpha zero state for '{mark}'")
                az_state.apply_action(index)

        # compute alpha zero's next move
        with Timer(text="AZS.bot.step took {:0.4f} seconds"):
            action = bot.step(az_state)

        # return the move as represented by our actual game
        return game_state.make_move_to(action)