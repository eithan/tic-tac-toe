import { memo, useCallback } from 'react';
import { PLAYER_TYPES, PLAYERS, GAME_STATUS, TIMING } from '../constants.js';

const GameBoard = memo(({ 
  board, 
  gameState, 
  gameStarted, 
  xPlayerType, 
  oPlayerType, 
  onMove 
}) => {
  const { status, current_player, winning_cells } = gameState;

  const handleMove = useCallback(async (index) => {
    const playerTypes = {
      x_player_type: xPlayerType,
      o_player_type: oPlayerType
    };

    // If game hasn't started yet and the first player is human, start the game first
    if (!gameStarted && xPlayerType === PLAYER_TYPES.HUMAN) {
      await onMove(index, true); // true indicates we need to start the game first
      return;
    }
    
    // If game hasn't started and first player is not human, show error
    if (!gameStarted && xPlayerType !== PLAYER_TYPES.HUMAN) {
      await onMove(index, false, "Click Play to Start!");
      return;
    }
    
    if (status !== GAME_STATUS.IN_PROGRESS) {
      await onMove(index, false, "Click Play to Start!");
      return;
    }
    
    const isCurrentPlayerHuman = (current_player === PLAYERS.X && xPlayerType === PLAYER_TYPES.HUMAN) || 
                                (current_player === PLAYERS.O && oPlayerType === PLAYER_TYPES.HUMAN);
    
    if (isCurrentPlayerHuman) {
      await onMove(index, false, null, playerTypes);
    } else {
      await onMove(index, false, "Click Play to Start!");
    }
  }, [gameStarted, xPlayerType, oPlayerType, status, current_player, onMove]);

  return (
    <div className="board">
      {board.map((cell, index) => {
        const isWinningCell = winning_cells && winning_cells.includes(index);
        const cellClass = `cell ${cell.toLowerCase()} ${gameStarted && status === GAME_STATUS.IN_PROGRESS ? `${current_player.toLowerCase()}-player` : ''} ${isWinningCell ? `winning-${cell.toLowerCase()}` : ''}`;
        
        const isCurrentPlayerHuman = (current_player === PLAYERS.X && xPlayerType === PLAYER_TYPES.HUMAN) || 
                                    (current_player === PLAYERS.O && oPlayerType === PLAYER_TYPES.HUMAN);
        
        const shouldShowHover = (gameStarted && cell === "" && status === GAME_STATUS.IN_PROGRESS && isCurrentPlayerHuman) ||
                               (!gameStarted && cell === "" && xPlayerType === PLAYER_TYPES.HUMAN);
        
        return (
          <button
            key={index}
            className={`${cellClass} ${shouldShowHover ? 'hover-enabled' : 'hover-disabled'}`}
            onClick={() => handleMove(index)}
          >
            {cell}
          </button>
        );
      })}
    </div>
  );
});

GameBoard.displayName = 'GameBoard';

export default GameBoard;
