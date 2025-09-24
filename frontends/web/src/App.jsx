// frontend/src/App.jsx
import { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
//const API_BASE_URL = "http://localhost:8000";
//const API_BASE_URL = "https://dialogic-unponderous-melody.ngrok-free.app";
console.log(API_BASE_URL)

function App() {
  const [gameState, setGameState] = useState(null);
  const [encodedState, setEncodedState] = useState(null);
  const [error, setError] = useState(null);
  const [xPlayerType, setXPlayerType] = useState("human");
  const [oPlayerType, setOPlayerType] = useState("human");
  const [gameStarted, setGameStarted] = useState(false);
  const [showClickError, setShowClickError] = useState(false);

  const fetchGameState = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/game_state`, {
        method: "POST",
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      });
      console.log(response.statusText)
      console.log(response)
      console.log(response.body)
      
      const data = await response.json();
      setGameState(data.game_state);
      setEncodedState(data.encoded_state);
    } catch (e) {
      console.log(e.message)
      setError("Failed to fetch game state.");
    }
  };

  const makeMove = async (index) => {
    try {
      const response = await fetch(`${API_BASE_URL}/game_move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          move: { index: index },
          encoded_state: encodedState,
          player_types: {
            x_player_type: xPlayerType,
            o_player_type: oPlayerType
          }
        }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to make move.");
      }
      const data = await response.json();
      setGameState(data.game_state);
      setEncodedState(data.encoded_state);
      setError(null);
      setShowClickError(false); // Clear click error on successful move
      return data.game_state;
    } catch (e) {
      setError(e.message);
      return null;
    }
  };

  const handleMove = async (index) => {
    // Clear any previous click error
    setShowClickError(false);
    
    // If game hasn't started yet and the first player is human, start the game first
    if (!gameStarted && xPlayerType === "human") {
      await startOrResetGame();
      // Wait a moment for the game to start, then make the move
      setTimeout(async () => {
        await makeMove(index);
      }, 100);
      return;
    }
    
    // If game hasn't started and first player is not human, show error
    if (!gameStarted && xPlayerType !== "human") {
      setShowClickError(true);
      return;
    }
    
    if (gameState.status !== "in_progress") {
      setShowClickError(true);
      return;
    }
    
    const currentPlayer = gameState.current_player;
    const isCurrentPlayerHuman = (currentPlayer === "X" && xPlayerType === "human") || 
                                (currentPlayer === "O" && oPlayerType === "human");
    
    if (isCurrentPlayerHuman) {
      await makeMove(index);
    } else {
      setShowClickError(true);
    }
  };

  const makeComputerMove = async () => {
    if (!gameState || gameState.status !== "in_progress") return;
    
    const currentPlayer = gameState.current_player;
    const isCurrentPlayerComputer = (currentPlayer === "X" && (xPlayerType === "random" || xPlayerType === "minimax" || xPlayerType === "alphazero")) || 
                                   (currentPlayer === "O" && (oPlayerType === "random" || oPlayerType === "minimax" || oPlayerType === "alphazero"));
    
    if (isCurrentPlayerComputer) {
      try {
        const response = await fetch(`${API_BASE_URL}/game_move`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            encoded_state: encodedState,
            player_types: {
              x_player_type: xPlayerType,
              o_player_type: oPlayerType
            }
          }),
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Failed to make computer move.");
        }
        const data = await response.json();
        setGameState(data.game_state);
        setEncodedState(data.encoded_state);
        setError(null);
      } catch (e) {
        setError(e.message);
      }
    }
  };

  const updatePlayerType = (player, newType) => {
    if (player === "X") {
      setXPlayerType(newType);
    } else {
      setOPlayerType(newType);
    }
  };

  const startOrResetGame = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/reset_game`, { method: "POST" });
      const data = await response.json();
      setGameState(data.game_state);
      setEncodedState(data.encoded_state);
      setGameStarted(true);
      setError(null);
      setShowClickError(false); // Clear any click error when starting game
    } catch (e) {
      setError("Failed to start/reset game.");
    }
  };

  useEffect(() => {
    fetchGameState();
  }, []);

  // Handle computer moves
  useEffect(() => {
    if (gameStarted && gameState && gameState.status === "in_progress") {
      const currentPlayer = gameState.current_player;
      const isCurrentPlayerComputer = (currentPlayer === "X" && (xPlayerType === "random" || xPlayerType === "minimax" || xPlayerType === "alphazero")) || 
                                     (currentPlayer === "O" && (oPlayerType === "random" || oPlayerType === "minimax" || oPlayerType === "alphazero"));
      
      if (isCurrentPlayerComputer) {
        const timer = setTimeout(() => {
          makeComputerMove();
        }, 200); // Small delay to make it feel more natural
        
        return () => clearTimeout(timer);
      }
    }
  }, [gameStarted, gameState, xPlayerType, oPlayerType]);

  if (!gameState) {
    return <div>Loading game...</div>;
  }

  const { board, message, status, current_player } = gameState;

  return (
    <div className="App">
      <h1>Tic-Tac-Toe</h1>
      <div className={`status-message ${showClickError ? 'error-message' : ''}`}>
        {showClickError ? 
          "Click Play to Start!" :
          (!gameStarted ? 
            (xPlayerType === "human" ? "Click any square to start playing!" : "Select players and click Play to start") 
            : message)
        }
      </div>
      {error && <div className="error-message">{error}</div>}
      
      <div className="player-selection">
        <div className="player-dropdown">
          <label htmlFor="x-player">X Player:</label>
          <select 
            id="x-player" 
            value={xPlayerType} 
            onChange={(e) => updatePlayerType("X", e.target.value)}
            disabled={gameStarted && gameState.status === "in_progress"}
          >
            <option value="human">Human</option>
            <option value="random">Random</option>
            <option value="minimax">Minimax</option>
            <option value="alphazero">AlphaZero</option>
          </select>
        </div>
        
        <div className="player-dropdown">
          <label htmlFor="o-player">O Player:</label>
          <select 
            id="o-player" 
            value={oPlayerType} 
            onChange={(e) => updatePlayerType("O", e.target.value)}
            disabled={gameStarted && gameState.status === "in_progress"}
          >
            <option value="human">Human</option>
            <option value="random">Random</option>
            <option value="minimax">Minimax</option>
            <option value="alphazero">AlphaZero</option>
          </select>
        </div>
      </div>
      
      <div className="board">
        {board.map((cell, index) => {
          const cellClass = `cell ${cell.toLowerCase()} ${gameStarted && status === "in_progress" ? `${current_player.toLowerCase()}-player` : ''}`;
          const isCurrentPlayerHuman = (current_player === "X" && xPlayerType === "human") || 
                                      (current_player === "O" && oPlayerType === "human");
          
          // Allow clicking if:
          // 1. Game is in progress and it's a human player's turn, OR
          // 2. Game hasn't started yet and the first player (X) is human, OR
          // 3. Always allow clicking to show error messages
          const isClickable = (gameStarted && cell === "" && status === "in_progress" && isCurrentPlayerHuman) ||
                             (!gameStarted && cell === "" && xPlayerType === "human") ||
                             true; // Always allow clicking to show error messages
          
          // Only show hover effects for valid moves, not for error messages
          const shouldShowHover = (gameStarted && cell === "" && status === "in_progress" && isCurrentPlayerHuman) ||
                                 (!gameStarted && cell === "" && xPlayerType === "human");
          
          return (
            <button
              key={index}
              className={`${cellClass} ${shouldShowHover ? 'hover-enabled' : 'hover-disabled'}`}
              onClick={() => handleMove(index)}
              disabled={false} // Never disable to allow error messages
            >
              {cell}
            </button>
          );
        })}
      </div>
      {!gameStarted || status !== "in_progress" ? (
        <button onClick={startOrResetGame} className="reset-button">
          {!gameStarted ? "Play" : "Play Again"}
        </button>
      ) : null}
    </div>
  );
}

export default App;

