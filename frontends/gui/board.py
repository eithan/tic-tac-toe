import tkinter as tk
from functools import partial
from tkinter import font
from .engine import TicTacToeUIEngine
from tic_tac_toe.logic.models import GameState
from tic_tac_toe.game.player_factory import PlayerFactory


class TicTacToeBoard(tk.Tk):
    """
    Creates a Tic-Tac-Toe board using tkinter UI

    Instantiate it and call play() method to start playing.
    Creates a UI thread that should run as the main thread.
    """

    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.title("Tic-Tac-Toe Game")
        self._selected_player_x: tk.StringVar
        self._selected_player_o: tk.StringVar
        self._cells = {}
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()
        self.engine = TicTacToeUIEngine(player_x_type=self._selected_player_x.get(),
                                        player_o_type=self._selected_player_o.get(),
                                        state_updated_listener=self._sync_game_state,
                                        ui_delay_callback=self._ui_delay)

    def play(self):
        """
        Play a game of Tic Tac Toe using the tkinter GUI.

        Handles initialization of the board and provides buttons for selecting player types and starting the game.
        """
        self._restart_game()
        self.mainloop()

    def _play_gui_move(self, position):
        mapped_position = TicTacToeBoard._position_to_index(position)
        self.engine.gui_move_to(mapped_position)

    def _restart_game(self):
        """
        Reset the game's board/engine to play again.

        This can take a bit of time as new computer players might be generated depending on selected player types.
        """
        self._update_display(msg="Ready?")
        self.config(cursor="wait")  # TODO this only applies to parts of window without widgets (?) apply to all?
        self.update()
        
        try:
            self.engine.prepare_new_game(self._selected_player_x.get(), self._selected_player_o.get())
            self.engine.process_next_action()
        except ValueError as e:
            # Show user-friendly error message
            error_msg = str(e)
            if "AlphaZero" in error_msg:
                self._update_display(msg="AlphaZero not available. Install neural network dependencies.")
            else:
                self._update_display(msg=f"Error: {error_msg}")
            # Reset to default players
            self._selected_player_x.set("Human")
            self._selected_player_o.set("Human")
            return
        
        self.config(cursor="")  # reset cursor to normal
        self.update()

    def _sync_game_state(self, game_state: GameState, gui_move_next: bool):
        # disable inputs while syncing unless it's the GUI's move
        self._configure_inputs(force_disabled=not gui_move_next)
        if gui_move_next: return  # nothing to sync if we are waiting for a GUI move

        # TODO: make this more efficient (unfortunately game_state doesn't tell me the last move)
        inv_map = {v: k for k, v in self._cells.items()}
        next_letter = 0
        for i in range(3):
            for j in range(3):
                letter = game_state.grid.cells[next_letter]
                button: tk.Button = inv_map[(i, j)]
                button.configure(text=letter, highlightbackground="lightblue")  # cells are lightblue before game_over
                next_letter += 1

        if game_state.game_over:
            self._highlight_cells(game_state)
            game_over_text = \
                f"{game_state.winner.value} wins \N{party popper}" if game_state.winner else f"Draw \N{neutral face}"
            self.display.config(text=game_over_text)
        else:
            current_player_mark = game_state.current_mark.value
            self.display.config(text=f"{current_player_mark}'s move")

    def _ui_delay(self, func):
        self.after(65, func)

    def _configure_inputs(self, force_disabled: bool):
        """Update buttons to enable or disable themselves based on state"""
        for button, position in self._cells.items():
            row, col = position
            is_disabled = force_disabled or button["text"] != " "  # TODO or game_state.game_over
            button.configure(state=tk.DISABLED if is_disabled else tk.NORMAL)
            button.configure(command=None if is_disabled else partial(self._play_gui_move, (row, col)))
            button.update_idletasks()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self._restart_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        # create the display frame for game messages to user
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

        # create the frame to choose player types and for the start button
        chooser_frame = tk.Frame(master=self)
        chooser_frame.pack(fill=tk.X, padx=10)
        element_width = 9
        
        # Get available player types dynamically
        available_computer_types = PlayerFactory.get_available_types()
        player_types = ["Human"] + [pt.title() for pt in available_computer_types]  # Capitalize for display

        # create dropdown to select X player
        sel_player_x = tk.StringVar(chooser_frame)
        sel_player_x.set(player_types[0])  # default value
        dropdown_x = tk.OptionMenu(chooser_frame, sel_player_x, *player_types)
        dropdown_x.config(width=element_width)
        dropdown_x.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._selected_player_x = sel_player_x

        play_button = tk.Button(master=chooser_frame, text="Start Game",
                                font=font.Font(size=14, weight="bold"), command=self._restart_game)
        play_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # create dropdown to select O player
        sel_player_o = tk.StringVar(chooser_frame)
        sel_player_o.set(player_types[0])  # default value
        dropdown_o = tk.OptionMenu(chooser_frame, sel_player_o, *player_types)
        dropdown_o.config(width=element_width)
        dropdown_o.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._selected_player_o = sel_player_o

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text=" ",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    disabledforeground="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                    command=partial(self._play_gui_move, (row, col))
                )
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                self._cells[button] = (row, col)

    def _update_display(self, msg):
        self.display["text"] = msg

    def _highlight_cells(self, game_state: GameState):
        for button, coordinates in self._cells.items():
            index = TicTacToeBoard._position_to_index(coordinates)
            if index in game_state.winning_cells:
                button.config(highlightbackground="green")

    @staticmethod
    def _position_to_index(position, num_cols=3):
        """Maps a (row, col) position in a 2x2 grid to a single col-wise index"""
        row, col = position
        return num_cols * row + col


if __name__ == "__main__":
    TicTacToeBoard().play()
