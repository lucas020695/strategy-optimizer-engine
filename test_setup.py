"""Test if all imports work"""
try:
    from src.optimizer import StrategyOptimizer
    from src.visualizer import StrategyVisualizer
    from src.strategies import MovingAverageCrossover
    print("✓ All imports successful!")
except ImportError as e:
    print(f"✗ Import error: {e}")
