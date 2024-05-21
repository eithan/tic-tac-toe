import numpy as np
import pyspiel
from codetiming import Timer
from open_spiel.python.algorithms import mcts

from open_spiel.python.algorithms.alpha_zero import evaluator as az_evaluator

from neuralnet.models.alphazeromodel import AlphaZeroModel
from tic_tac_toe.game.players import ComputerPlayer
from tic_tac_toe.logic.models import GameState, Move, Mark


class AlphaZeroComputerPlayer(ComputerPlayer):
    @Timer(text="AZ.init took {:0.4f} seconds")
    def __init__(self, mark: Mark):
        """
        Creates an Alpha Zero computer player in the format required by our actual game.
        Loading the model takes a little bit of time.

        Loads the trained model from a file distributed with this application.
        Holds its own game state for syncing with our actual game.
        """
        super().__init__(mark)
        game = pyspiel.load_game("tic_tac_toe")
        evaluator = az_evaluator.AlphaZeroEvaluator(game, AlphaZeroModel())
        self._state = game.new_initial_state()

        self._bot = mcts.MCTSBot(
            game,
            2,
            50,  # TODO what is optimal here? they had 10000 but it takes much longer to play
            evaluator,
            random_state=np.random.RandomState(),
            child_selection_fn=mcts.SearchNode.puct_value,
            solve=True,
            verbose=False)

    def get_computer_move(self, game_state: GameState) -> Move | None:
        """
        Alpha Zero computes its next Tic-Tac-Toe move

        First we retrieve our internal history of moves.
        Next we sync with the actual game state.
        Then we compute our move.
        Finally we convert our move to the actual game representation and return it.
        """
        # this is alpha zero's history
        history = self._state.history()

        # loop through our actual game state grid
        for index in range(0, len(game_state.grid.cells)):
            c = game_state.grid.cells[index]

            # if there was a move made and alpha zero has no record of it, apply the move
            if c != " " and index not in history:
                self._state.apply_action(index)

        # compute alpha zero's next move and apply it to alpha zero's internal state (TODO optimize this more?)
        with Timer(text="AZ.bot.step took {:0.4f} seconds"):
            action = self._bot.step(self._state)
        self._state.apply_action(action)

        # return the move as represented by our actual game
        return game_state.make_move_to(action)
