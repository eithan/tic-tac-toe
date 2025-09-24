import { memo } from 'react';
import { PLAYER_TYPES } from '../constants.js';

const PlayerSelection = memo(({ xPlayerType, oPlayerType, onPlayerTypeChange, gameStarted, gameInProgress }) => {
  const isDisabled = gameStarted && gameInProgress;

  return (
    <div className="player-selection">
      <div className="player-dropdown">
        <label htmlFor="x-player">X Player:</label>
        <select 
          id="x-player" 
          value={xPlayerType} 
          onChange={(e) => onPlayerTypeChange("X", e.target.value)}
          disabled={isDisabled}
        >
          <option value={PLAYER_TYPES.HUMAN}>Human</option>
          <option value={PLAYER_TYPES.RANDOM}>Random</option>
          <option value={PLAYER_TYPES.MINIMAX}>Minimax</option>
          <option value={PLAYER_TYPES.ALPHAZERO}>AlphaZero</option>
        </select>
      </div>
      
      <div className="player-dropdown">
        <label htmlFor="o-player">O Player:</label>
        <select 
          id="o-player" 
          value={oPlayerType} 
          onChange={(e) => onPlayerTypeChange("O", e.target.value)}
          disabled={isDisabled}
        >
          <option value={PLAYER_TYPES.HUMAN}>Human</option>
          <option value={PLAYER_TYPES.RANDOM}>Random</option>
          <option value={PLAYER_TYPES.MINIMAX}>Minimax</option>
          <option value={PLAYER_TYPES.ALPHAZERO}>AlphaZero</option>
        </select>
      </div>
    </div>
  );
});

PlayerSelection.displayName = 'PlayerSelection';

export default PlayerSelection;
