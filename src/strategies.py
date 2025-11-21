"""Example trading strategies"""

import numpy as np
import pandas as pd
from typing import Tuple


class MovingAverageCrossover:
    """Simple moving average crossover strategy"""

    @staticmethod
    def run(data: pd.DataFrame, params: dict) -> Tuple[pd.Series, pd.DataFrame]:
        """
        Run MA crossover strategy

        Args:
            data: DataFrame with OHLCV (close required)
            params: {fast_window, slow_window}

        Returns:
            (returns, trades)
        """
        close = data['close'].copy()
        fast_window = int(params.get('fast_window', 10))
        slow_window = int(params.get('slow_window', 30))

        # Calculate moving averages
        fast_ma = close.rolling(window=fast_window).mean()
        slow_ma = close.rolling(window=slow_window).mean()

        # Generate signals
        signal = np.where(fast_ma > slow_ma, 1, -1)
        signal = pd.Series(signal, index=close.index)

        # Calculate returns
        returns = close.pct_change() * signal.shift(1)
        returns = returns.fillna(0)

        # Cumulative return
        cumulative_returns = (1 + returns).cumprod() * 100

        # Create trades record
        trades = pd.DataFrame({
            'pnl': returns,
            'position': signal
        })

        return cumulative_returns, trades


class MeanReversion:
    """Mean reversion strategy based on z-score"""
    
    @staticmethod
    def run(data: pd.DataFrame, params: dict) -> Tuple[pd.Series, pd.DataFrame]:
        """
        Run mean reversion strategy
        
        Args:
            data: DataFrame with OHLCV
            params: {lookback, zscore_threshold, position_size}
        
        Returns:
            (returns, trades)
        """
        close = data['close'].copy()
        lookback = int(params.get('lookback', 20))
        zscore_thresh = params.get('zscore_threshold', 2.0)
        pos_size = params.get('position_size', 0.95)
        
        # Calculate mean and std
        rolling_mean = close.rolling(window=lookback).mean()
        rolling_std = close.rolling(window=lookback).std()
        
        # Z-score
        zscore = (close - rolling_mean) / rolling_std
        
        # Generate signals
        signal = np.where(zscore < -zscore_thresh, 1,  # Buy oversold
                         np.where(zscore > zscore_thresh, -1,  # Sell overbought
                                 0))  # Hold
        signal = pd.Series(signal, index=close.index)
        signal = signal.fillna(method='ffill')
        
        # Calculate returns
        returns = close.pct_change() * (signal.shift(1) * pos_size)
        returns = returns.fillna(0)
        
        # Cumulative return
        cumulative_returns = (1 + returns).cumprod() * 100
        
        trades = pd.DataFrame({
            'pnl': returns,
            'position': signal,
            'zscore': zscore
        })
        
        return cumulative_returns, trades


class VolatilityBreakout:
    """Volatility breakout strategy"""
    
    @staticmethod
    def run(data: pd.DataFrame, params: dict) -> Tuple[pd.Series, pd.DataFrame]:
        """
        Run volatility breakout strategy
        
        Args:
            data: DataFrame with OHLCV
            params: {lookback, multiplier, min_volatility}
        
        Returns:
            (returns, trades)
        """
        close = data['close'].copy()
        high = data['high'].copy()
        low = data['low'].copy()
        
        lookback = int(params.get('lookback', 20))
        multiplier = params.get('multiplier', 1.5)
        min_vol = params.get('min_volatility', 0.001)
        
        # Calculate ATR (Average True Range)
        tr = np.maximum(
            high - low,
            np.maximum(
                np.abs(high - close.shift(1)),
                np.abs(low - close.shift(1))
            )
        )
        atr = tr.rolling(window=lookback).mean()
        
        # Volatility filter
        volatility = close.pct_change().rolling(window=lookback).std()
        
        # Generate breakout signals
        high_band = high.rolling(window=lookback).max()
        low_band = low.rolling(window=lookback).min()
        
        signal = np.where(
            (close > high_band.shift(1)) & (volatility > min_vol),
            1,
            np.where(
                (close < low_band.shift(1)) & (volatility > min_vol),
                -1,
                0
            )
        )
        signal = pd.Series(signal, index=close.index)
        signal = signal.fillna(method='ffill')
        
        # Calculate returns
        returns = close.pct_change() * signal.shift(1)
        returns = returns.fillna(0)
        
        # Cumulative return
        cumulative_returns = (1 + returns).cumprod() * 100
        
        trades = pd.DataFrame({
            'pnl': returns,
            'position': signal,
            'volatility': volatility
        })
        
        return cumulative_returns, trades


class RSIStrategy:
    """Relative Strength Index strategy"""
    
    @staticmethod
    def run(data: pd.DataFrame, params: dict) -> Tuple[pd.Series, pd.DataFrame]:
        """
        Run RSI strategy
        
        Args:
            data: DataFrame with OHLCV
            params: {rsi_period, oversold_threshold, overbought_threshold}
        
        Returns:
            (returns, trades)
        """
        close = data['close'].copy()
        period = int(params.get('rsi_period', 14))
        oversold = params.get('oversold_threshold', 30)
        overbought = params.get('overbought_threshold', 70)
        
        # Calculate RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Generate signals
        signal = np.where(rsi < oversold, 1,      # Buy oversold
                         np.where(rsi > overbought, -1,  # Sell overbought
                                 0))  # Hold
        signal = pd.Series(signal, index=close.index)
        signal = signal.fillna(method='ffill')
        
        # Calculate returns
        returns = close.pct_change() * signal.shift(1)
        returns = returns.fillna(0)
        
        # Cumulative return
        cumulative_returns = (1 + returns).cumprod() * 100
        
        trades = pd.DataFrame({
            'pnl': returns,
            'position': signal,
            'rsi': rsi
        })
        
        return cumulative_returns, trades
