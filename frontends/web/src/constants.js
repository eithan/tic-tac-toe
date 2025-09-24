// Game configuration constants
export const PLAYER_TYPES = {
  HUMAN: 'human',
  RANDOM: 'random',
  MINIMAX: 'minimax',
  ALPHAZERO: 'alphazero'
};

export const GAME_STATUS = {
  IN_PROGRESS: 'in_progress',
  FINISHED: 'finished'
};

export const PLAYERS = {
  X: 'X',
  O: 'O'
};

export const COMPUTER_PLAYER_TYPES = [PLAYER_TYPES.RANDOM, PLAYER_TYPES.MINIMAX, PLAYER_TYPES.ALPHAZERO];

export const API_ENDPOINTS = {
  GAME_STATE: '/game_state',
  GAME_MOVE: '/game_move',
  RESET_GAME: '/reset_game'
};

export const TIMING = {
  COMPUTER_MOVE_DELAY: 200, // ms
  GAME_START_DELAY: 100 // ms
};

export const BOARD_SIZE = 9; // 3x3 grid
