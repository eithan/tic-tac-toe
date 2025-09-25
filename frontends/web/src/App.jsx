// frontend/src/App.jsx
import { useState, useEffect, useCallback, memo } from 'react';
import './App.css';
import { useGameLogic } from './hooks/useGameLogic.js';
import { useComputerMoves } from './hooks/useComputerMoves.js';
import PlayerSelection from './components/PlayerSelection.jsx';
import GameBoard from './components/GameBoard.jsx';
import StatusMessage from './components/StatusMessage.jsx';
import { PLAYER_TYPES, GAME_STATUS, TIMING } from './constants.js';
import { config } from './config/environment.js';

const App = memo(() => {
  const [xPlayerType, setXPlayerType] = useState(PLAYER_TYPES.HUMAN);
  const [oPlayerType, setOPlayerType] = useState(PLAYER_TYPES.HUMAN);
  const [showClickError, setShowClickError] = useState(false);

  const {
    gameState,
    encodedState,
    error,
    gameStarted,
    setGameStarted,
    setError,
    fetchGameState,
    makeMove,
    makeComputerMove,
    resetGame,
    isCurrentPlayerHuman
  } = useGameLogic();

  // Memoized callbacks to prevent unnecessary re-renders
  const updatePlayerType = useCallback((player, newType) => {
    if (player === "X") {
      setXPlayerType(newType);
    } else {
      setOPlayerType(newType);
    }
  }, []);

  const handleMove = useCallback(async (index, shouldStartGame = false, errorMessage = null, playerTypes = null) => {
    setShowClickError(false);
    
    if (errorMessage) {
      setShowClickError(true);
      return;
    }

    if (shouldStartGame) {
      await resetGame();
      setTimeout(async () => {
        await makeMove(index, playerTypes);
      }, TIMING.GAME_START_DELAY);
      return;
    }

    await makeMove(index, playerTypes);
  }, [makeMove, resetGame]);

  const handleResetGame = useCallback(async () => {
    await resetGame();
    setShowClickError(false);
  }, [resetGame]);

  // Initialize game state
  useEffect(() => {
    fetchGameState();
  }, [fetchGameState]);

  // Handle computer moves using custom hook
  useComputerMoves(gameStarted, gameState, xPlayerType, oPlayerType, makeComputerMove);

  if (!gameState) {
    return <div>Loading game...(API: {config.API_BASE_URL})</div>;
  }

  const { board, message, status } = gameState;

  return (
    <div className="App">
      <h1>Tic-Tac-Toe</h1>
      
      <StatusMessage 
        showClickError={showClickError}
        gameStarted={gameStarted}
        xPlayerType={xPlayerType}
        message={message}
      />
      
      {error && <div className="error-message">{error}</div>}
      
      <PlayerSelection
        xPlayerType={xPlayerType}
        oPlayerType={oPlayerType}
        onPlayerTypeChange={updatePlayerType}
        gameStarted={gameStarted}
        gameInProgress={status === GAME_STATUS.IN_PROGRESS}
      />
      
      <GameBoard
        board={board}
        gameState={gameState}
        gameStarted={gameStarted}
        xPlayerType={xPlayerType}
        oPlayerType={oPlayerType}
        onMove={handleMove}
      />
      
      {!gameStarted || status !== GAME_STATUS.IN_PROGRESS ? (
        <button onClick={handleResetGame} className="reset-button">
          {!gameStarted ? "Play" : "Play Again"}
        </button>
      ) : null}
    </div>
  );
});

export default App;

