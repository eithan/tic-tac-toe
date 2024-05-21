from typing import TypeAlias, Callable

from tic_tac_toe.game.players import Player, RandomComputerPlayer, MinimaxComputerPlayer
from tic_tac_toe.logic.models import GameState, Mark, Move, Grid
from tic_tac_toe.logic.validators import validate_players
from neuralnet.models.players import AlphaZeroComputerPlayer


""" First parameter is the current game state to sync to; second parameter is whether it is the gui's turn to move """
StateUpdatedCallback: TypeAlias = Callable[[GameState, bool], None]

""" Parameter is a callable method to invoke after delay """
UIIDelayCallback: TypeAlias = Callable[[Callable], None]


class GUIPlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        # return None to indicate that this player will make a move through the UI
        return None


class TicTacToeUIEngine:
    # human-readable labels pointing to respective classes in order to fetch their constructor for a new instance
    PLAYER_TYPES = {
        "Human": GUIPlayer,
        "Random": RandomComputerPlayer,
        "Minimax": MinimaxComputerPlayer,
        "AlphaZero": AlphaZeroComputerPlayer
    }

    game_state: GameState
    player1: Player
    player2: Player

    def __init__(self, player_x_type: str,
                 player_o_type: str,
                 state_updated_listener: StateUpdatedCallback,
                 ui_delay_callback: UIIDelayCallback = None):
        """
        Construct a TicTacToeUIEngine.

        e.g.
        self.engine = TicTacToeUIEngine(player_x_type="Human",
                                        player_o_type="Random",
                                        state_updated_listener=self.sync_game_state,
                                        ui_delay_callback=self._ui_delay)

        player_x_type : str; X player type; must be one of PLAYER_TYPES keys
        player_x_type : str; O player type; must be one of PLAYER_TYPES keys
        state_updated_listener : StateUpdatedCallback; called whenever game state changes
                                 e.g. def sync_game_state(self, game_state: GameState, gui_move_next: bool): ...
        ui_delay_callback : UIIDelayCallback; allow for the UI to process before invoking a function
                            e.g. def _ui_delay(self, func): self.after(75, func)
        """
        self.state_updated_listener = state_updated_listener
        self.ui_delay_callback = ui_delay_callback
        self.prepare_new_game(player_x_type, player_o_type)

    def prepare_new_game(self, player_x_type: str, player_o_type: str):
        self.player1 = self._new_player(player_x_type, Mark("X"))
        self.player2 = self._new_player(player_o_type, Mark("O"))
        validate_players(self.player1, self.player2)
        self.game_state = GameState(Grid(), self.player1.mark)
        self._state_updated()

    def process_next_action(self):
        if self.game_state.game_over:
            self._state_updated()
        else:
            self._ui_delay(self._next_player_move)

    def gui_move_to(self, position):
        move = self.game_state.make_move_to(position)
        self._play_move(move)

    def _current_player(self):
        return self.player1 if self.game_state.current_mark == self.player1.mark else self.player2

    def _new_player(self, player_type: str, mark: Mark) -> Player | None:
        """ Instantiates a new player with the specified mark if a constructor is fetched, else returns None """
        class_constructor = self.PLAYER_TYPES.get(player_type)
        instance = class_constructor(mark) if class_constructor is not None else None
        return instance

    def _state_updated(self, gui_move_next: bool = False):
        if callable(self.state_updated_listener):
            self.state_updated_listener(self.game_state, gui_move_next)

    def _next_player_move(self):
        player = self._current_player()
        move = player.get_move(self.game_state)
        if move is not None:
            # computer player, so just play the move they computed
            self._play_move(move)
        else:
            # re-enable inputs for GUI player
            self._state_updated(gui_move_next=True)

    def _play_move(self, move: Move):
        self.game_state = move.after_state
        self._state_updated()
        self._ui_delay(self.process_next_action)

    def _ui_delay(self, method):
        """ Executes the passed in method on the UI delay callback if available, else calls method immediately """
        if method is None or not callable(method): return
        if self.ui_delay_callback is not None and callable(self.ui_delay_callback):
            self.ui_delay_callback(method)
        else:
            method()
