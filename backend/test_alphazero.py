#!/usr/bin/env python3
"""
Test script to check AlphaZero availability
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from tic_tac_toe.game.player_factory import PlayerFactory
    print("✅ PlayerFactory imported successfully")
    
    factory = PlayerFactory()
    player_types = factory.get_available_types()
    print(f"📋 Available player types: {player_types}")
    
    if "alphazero" in player_types:
        print("✅ AlphaZero is available!")
        
        # Try to create an AlphaZero player
        try:
            player = factory.create_player("alphazero", "X")
            print(f"✅ AlphaZero player created: {type(player).__name__}")
        except Exception as e:
            print(f"❌ Failed to create AlphaZero player: {e}")
    else:
        print("❌ AlphaZero is not available")
        
        # Check what's causing the issue
        try:
            import neuralnet
            print("✅ neuralnet package is available")
        except ImportError as e:
            print(f"❌ neuralnet package not available: {e}")
            
        try:
            import tensorflow
            print("✅ TensorFlow is available")
        except ImportError as e:
            print(f"❌ TensorFlow not available: {e}")
            
        try:
            import open_spiel
            print("✅ OpenSpiel is available")
        except ImportError as e:
            print(f"❌ OpenSpiel not available: {e}")

except Exception as e:
    print(f"❌ Error importing PlayerFactory: {e}")
    import traceback
    traceback.print_exc()
