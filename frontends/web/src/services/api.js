import { API_ENDPOINTS } from '../constants.js';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    };

    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async fetchGameState(encodedState = null) {
    const body = encodedState ? { encoded_state: encodedState } : {};
    return this.makeRequest(API_ENDPOINTS.GAME_STATE, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  }

  async makeMove(move, encodedState, playerTypes) {
    return this.makeRequest(API_ENDPOINTS.GAME_MOVE, {
      method: 'POST',
      body: JSON.stringify({
        move: { index: move },
        encoded_state: encodedState,
        player_types: playerTypes
      })
    });
  }

  async makeComputerMove(encodedState, playerTypes) {
    return this.makeRequest(API_ENDPOINTS.GAME_MOVE, {
      method: 'POST',
      body: JSON.stringify({
        encoded_state: encodedState,
        player_types: playerTypes
      })
    });
  }

  async resetGame() {
    return this.makeRequest(API_ENDPOINTS.RESET_GAME, {
      method: 'POST'
    });
  }
}

export const apiService = new ApiService();
