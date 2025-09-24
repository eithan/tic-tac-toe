import { useState, useCallback } from 'react';
import { apiService } from '../services/api.js';
import { PLAYER_TYPES, PLAYERS, TIMING } from '../constants.js';

export const useGameLogic = () => {
  const [gameState, setGameState] = useState(null);
  const [encodedState, setEncodedState] = useState(null);
  const [error, setError] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);

  const updateGameState = useCallback((data) => {
    setGameState(data.game_state);
    setEncodedState(data.encoded_state);
    setError(null);
  }, []);

  const fetchGameState = useCallback(async () => {
    try {
      const data = await apiService.fetchGameState();
      updateGameState(data);
    } catch (e) {
      setError("Failed to fetch game state.");
    }
  }, [updateGameState]);

  const makeMove = useCallback(async (index, playerTypes) => {
    try {
      const data = await apiService.makeMove(index, encodedState, playerTypes);
      updateGameState(data);
      return data.game_state;
    } catch (e) {
      setError(e.message);
      return null;
    }
  }, [encodedState, updateGameState, setError]);

  const makeComputerMove = useCallback(async (playerTypes) => {
    try {
      const data = await apiService.makeComputerMove(encodedState, playerTypes);
      updateGameState(data);
    } catch (e) {
      setError(e.message);
    }
  }, [encodedState, updateGameState, setError]);

  const resetGame = useCallback(async () => {
    try {
      const data = await apiService.resetGame();
      updateGameState(data);
      setGameStarted(true);
    } catch (e) {
      setError("Failed to start/reset game.");
    }
  }, [updateGameState, setGameStarted, setError]);

  const isPlayerType = useCallback((player, playerType) => {
    return player === playerType;
  }, []);

  const isCurrentPlayerHuman = useCallback((currentPlayer, xPlayerType, oPlayerType) => {
    return (currentPlayer === PLAYERS.X && isPlayerType(xPlayerType, PLAYER_TYPES.HUMAN)) ||
           (currentPlayer === PLAYERS.O && isPlayerType(oPlayerType, PLAYER_TYPES.HUMAN));
  }, [isPlayerType]);

  const isCurrentPlayerComputer = useCallback((currentPlayer, xPlayerType, oPlayerType) => {
    return (currentPlayer === PLAYERS.X && xPlayerType !== PLAYER_TYPES.HUMAN) ||
           (currentPlayer === PLAYERS.O && oPlayerType !== PLAYER_TYPES.HUMAN);
  }, []);

  return {
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
    isCurrentPlayerHuman,
    isCurrentPlayerComputer
  };
};
