import { memo } from 'react';
import { PLAYER_TYPES } from '../constants.js';

const StatusMessage = memo(({ showClickError, gameStarted, xPlayerType, message }) => {
  const getStatusMessage = () => {
    if (showClickError) {
      return "Click Play to Start!";
    }
    
    if (!gameStarted) {
      return xPlayerType === PLAYER_TYPES.HUMAN 
        ? "Click any square to start playing!" 
        : "Select players and click Play to start";
    }
    
    return message;
  };

  return (
    <div className={`status-message ${showClickError ? 'error-message' : ''}`}>
      {getStatusMessage()}
    </div>
  );
});

StatusMessage.displayName = 'StatusMessage';

export default StatusMessage;
