import { useEffect } from 'react';
import { PLAYER_TYPES, GAME_STATUS, TIMING } from '../constants.js';

export const useComputerMoves = (gameStarted, gameState, xPlayerType, oPlayerType, makeComputerMove) => {
  useEffect(() => {
    if (!gameStarted || !gameState || gameState.status !== GAME_STATUS.IN_PROGRESS) {
      return;
    }

    const currentPlayer = gameState.current_player;
    const isCurrentPlayerComputer = (currentPlayer === 'X' && xPlayerType !== PLAYER_TYPES.HUMAN) ||
                                   (currentPlayer === 'O' && oPlayerType !== PLAYER_TYPES.HUMAN);

    if (isCurrentPlayerComputer) {
      const timer = setTimeout(() => {
        makeComputerMove({
          x_player_type: xPlayerType,
          o_player_type: oPlayerType
        });
      }, TIMING.COMPUTER_MOVE_DELAY);

      return () => clearTimeout(timer);
    }
  }, [gameStarted, gameState, xPlayerType, oPlayerType, makeComputerMove]);
};
