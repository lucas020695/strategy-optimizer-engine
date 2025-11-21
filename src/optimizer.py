"""
Strategy Parameter Optimizer Framework
A scientific tool for parameter optimization across any trading strategy
"""

import logging
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from typing import Callable, Dict, Tuple
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


class ParameterOptimizer:
    """Scientific framework for strategy parameter optimization"""

    def __init__(self, market_data: pd.DataFrame):
        self.market_data = market_data
        self.results = []

    def optimize(self,
                 strategy_func: Callable,
                 param_space: Dict[str, Tuple[int, int, int]],
                 metric: str = 'sharpe_ratio') -> Dict:
        """
        Optimize parameters using grid search

        Args:
            strategy_func: Function that takes (data, **params) and returns metrics dict
            param_space: {'param_name': (min, max, step)}
            metric: Which metric to optimize for

        Returns:
            {'best_params': {}, 'best_score': float, 'results': []}
        """

        logger.info("=" * 70)
        logger.info("PARAMETER OPTIMIZATION - Grid Search")
        logger.info("=" * 70)

        best_score = -999
        best_params = None

        param_names = list(param_space.keys())
        param_ranges = [np.arange(v[0], v[1] + v[2], v[2]) for v in param_space.values()]

        import itertools
        combos = list(itertools.product(*param_ranges))

        logger.info(f"\nTesting {len(combos)} parameter combinations...\n")

        for i, combo in enumerate(combos, 1):
            params = {param_names[j]: combo[j] for j in range(len(param_names))}

            try:
                metrics = strategy_func(self.market_data, **params)

                if metrics and metric in metrics:
                    score = metrics[metric]
                    self.results.append({'params': params, **metrics})

                    if score > best_score:
                        best_score = score
                        best_params = params
                        logger.info(f"   [{i}/{len(combos)}] New best {metric}: {score:.4f} | params: {params}")

            except Exception as e:
                logger.debug(f"   Combo failed: {e}")
                continue

        return {
            'best_params': best_params,
            'best_score': best_score,
            'results': self.results
        }

    def plot_3d_landscape(self,
                          param_x: str,
                          param_y: str,
                          metric: str = 'sharpe_ratio',
                          title: str = 'Parameter Optimization Landscape'):
        """Visualize 2D parameter landscape in 3D with Matplotlib"""

        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        # Flatten results
        flattened = []
        for result in self.results:
            params = result.copy()
            params.pop('params', None)
            param_dict = result.get('params', {})
            flattened.append({**param_dict, **params})

        df = pd.DataFrame(flattened)

        # Pivot for surface
        pivot = df.pivot_table(
            values=metric,
            index=param_y,
            columns=param_x,
            aggfunc='max'
        )

        # Create 3D plot
        fig = plt.figure(figsize=(14, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Create mesh
        x_data = pivot.columns.values
        y_data = pivot.index.values
        X, Y = np.meshgrid(x_data, y_data)
        Z = pivot.values

        # Plot surface
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.8)

        # Labels
        ax.set_xlabel(f'{param_x}', fontsize=11, fontweight='bold')
        ax.set_ylabel(f'{param_y}', fontsize=11, fontweight='bold')
        ax.set_zlabel(f'{metric}', fontsize=11, fontweight='bold')
        ax.set_title(f'{title}', fontsize=13, fontweight='bold', pad=20)

        # Colorbar
        fig.colorbar(surf, ax=ax, pad=0.1, label=metric)

        # Camera angle
        ax.view_init(elev=25, azim=45)

        plt.tight_layout()
        plt.savefig('optimization_landscape.png', dpi=300, bbox_inches='tight')
        logger.info("3D landscape saved as 'optimization_landscape.png'")
        plt.show()


def rsi_strategy(data: pd.DataFrame, rsi_period: int, overbought: int, oversold: int) -> Dict:
    """RSI oversold/overbought strategy"""

    close = data['Close'].squeeze()

    # Calculate RSI
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Signal
    signal = np.where(rsi < oversold, 1, np.where(rsi > overbought, -1, 0))
    sig_series = pd.Series(signal, index=close.index)
    sig_series = sig_series.fillna(method='ffill').fillna(0)

    # Returns
    ret = close.pct_change() * sig_series.shift(1)
    ret = ret.fillna(0)

    equity = (1 + ret).cumprod()

    # Metrics
    daily_ret = ret.dropna()
    if len(daily_ret) > 50 and daily_ret.std() > 0:
        sharpe = (daily_ret.mean() / daily_ret.std()) * np.sqrt(252)
        total_return = (equity.iloc[-1] / equity.iloc[0] - 1) * 100
        max_dd = ((equity / equity.expanding().max() - 1).min()) * 100

        return {
            'sharpe_ratio': float(sharpe),
            'total_return': float(total_return),
            'max_drawdown': float(max_dd),
            'num_trades': float((sig_series.diff() != 0).sum())
        }

    return None


def main():
    """Run framework on Bitcoin"""

    logger.info("\nLoading market data...")

    import yfinance as yf
    data = yf.download('BTC-USD', start='2020-01-01', end='2024-12-31', progress=False)

    logger.info(f"Loaded {len(data)} days of data\n")

    # Initialize optimizer
    opt = ParameterOptimizer(data)

    # Define parameter space
    param_space = {
        'rsi_period': (10, 30, 5),
        'overbought': (60, 80, 5),
        'oversold': (20, 40, 5)
    }

    # Run optimization
    results = opt.optimize(
        strategy_func=rsi_strategy,
        param_space=param_space,
        metric='sharpe_ratio'
    )

    # Print best result
    logger.info(f"\n{'='*70}")
    logger.info("OPTIMIZATION COMPLETE")
    logger.info(f"{'='*70}\n")

    if results['best_score'] > 0:
        logger.info(f"Best Sharpe Ratio: {results['best_score']:.4f}")
        logger.info(f"Best Parameters: {results['best_params']}\n")

        # Visualize
        opt.plot_3d_landscape(
            param_x='rsi_period',
            param_y='overbought',
            metric='sharpe_ratio',
            title='Bitcoin RSI Strategy - Parameter Landscape'
        )
    else:
        logger.info("No profitable parameters found")


if __name__ == '__main__':
    main()
