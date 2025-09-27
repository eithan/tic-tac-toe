# Tic-Tac-Toe

In this project you will find a Tic-Tac-Toe game that is extensible to allow 
other frontends and player types. \
The original code is located [here](https://realpython.com/tic-tac-toe-ai-python/), and was slightly adapted/extended to support 
a Tkinter GUI (also adapted from a source below) and an AlphaZero AI player.

### Installing

From top-level project folder, create/activate a virtual environment and 
pip install the requirements.txt file. This will install the adapted
tic-tac-toe library included in the source as an editable library.

NOTE: these might need to be installed for TKinter to run properly, then re-install Python 3.12.5
`brew install openssl readline sqlite3 xz zlib tcl-tk`

e.g. using pyenv and Python 3.12.5: \
`pyenv virtualenv 3.12.5 tic-tac-toe-3.12.5` \
`pyenv activate tic-tac-toe-3.12.5` \
`pip install -r requirements.txt`

### Running (Tkinter GUI or Console)

Run GUI from top-level project folder:\
`python -m frontends.gui`

Run console from top-level project folder (see more options below): \
`python -m frontends.console -X human -O alphazero`

options: \
  `-h, --help            show this help message and exit` \
  `-X {human,random,minimax,alphazero}` \
  `-O {human,random,minimax,alphazero}` \
  `--starting {Mark.CROSS,Mark.NAUGHT}`


### Code

The new code is primarily located in `frontends/gui` and `lib-tic-tac-toe-ai/`.

The Tkinter GUI code was adapted from [here](https://realpython.com/tic-tac-toe-python/) with the following changes:

* It was modified to use the game logic from a different game implementation of Tic-Tac-Toe.
* It was modified to allow player type selection with a start button.
  * Human, Random, Minimax, AlphaZero

The AlphaZero code uses the amazing open-spiel library and was adapted from their example [here](https://github.com/google-deepmind/open_spiel/blob/master/open_spiel/python/examples/tic_tac_toe_alpha_zero.py).

* First it was trained on some number of iterations to generate a model (see `lib-tic-tac-toe-ai/training/tic_tac_toe_alpha_zero.py`)
* Then the generated model was stored for loading by the game when needed (see `lib-tic-tac-toe-ai/src/tic_tac_toe/models/az_model`).
* An AI player was created called AlphaZeroComputerPlayer that loads the trained model, syncs with the real game state, and proposes the next move when it has a turn.

Sincere thanks to the tutorial authors from realpython.com mentioned in the source below!

### Training AlphaZero

!! First off, there is a bug in the latest version of OpenSpiel at the time of writing this code.
In order for training to work, you MUST modify your open_spiel code per the solution in the github issue at https://github.com/google-deepmind/open_spiel/issues/1206.
If not, you will get a TensorFlow error and not be able to train your model.

NOTE: You do NOT need to run this code, but if you are interested in how the AlphaZero model was trained to play tic-tac-toe
you can run the OpenSpiel sample, modified slightly and stored in this repo, as follows:

`cd lib-tic-tac-toe-ai/training` \
`python tic_tac_toe_alpha_zero.py -path "./checkpoints"` \
`cp ./checkpoints/checkpoint--1* ../src/tic_tac_toe_ai/models/az_model/`

This will save the generated model, along with checkpoints and logs, in the path specified above.
The last line will copy the `checkpoint--1.*` files to `lib-tic-tac-toe-ai/src/tic_tac_toe_ai/models/az_model` to use your latest trained model in the game. \
`lib-tic-tac-toe-ai/src/tic_tac_toe_ai/models/alphazeromodel.py` is where the trained model is loaded into AlphaZero.

### Sources

https://realpython.com/tic-tac-toe-ai-python/ \
Python tutorial for writing an extensible Tic-Tac-Toe game/library with best practices interspersed.

https://realpython.com/tic-tac-toe-python/ \
Python tutorial for developing a Tic-Tac-Toe game with a Tkinter UI. 

https://openspiel.readthedocs.io/en/stable/alpha_zero.html#python \
Open-Spiel documentation and [sample code](https://github.com/google-deepmind/open_spiel/blob/master/open_spiel/python/examples/tic_tac_toe_alpha_zero.py) for training an AlphaZero agent to play Tic-Tac-Toe.