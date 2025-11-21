import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import graph_objects as go
import plotly.express as px
import logging

logger = logging.getLogger(__name__)


class StrategyVisualizer:

    def __init__(self, theme: str = 'plotly'):
        self.theme = theme
        sns.set_style("darkgrid")
        plt.rcParams['figure.figsize'] = (14, 8)

    def plot_3d_surface(
        self,
        x_values: np.ndarray,
        y_values: np.ndarray,
        z_values: np.ndarray,
        title: str = "Parameter Optimization Surface"
    ):

        X, Y = np.meshgrid(x_values, y_values)

        fig = go.Figure(data=[go.Surface(z=z_values, x=X, y=Y, colorscale='Viridis')])

        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Fast Window',
                yaxis_title='Slow Window',
                zaxis_title='Sharpe Ratio'
            ),
            width=1200,
            height=800,
            template=self.theme
        )

        fig.show()
        logger.info("✓ 3D surface plot created")

    def plot_equity_curves(
        self,
        returns1: pd.Series,
        returns2: pd.Series,
        label1: str = "Strategy 1",
        label2: str = "Strategy 2",
        title: str = "Equity Curves Comparison"
    ):

        cum1 = (1 + returns1.pct_change()).cumprod() * 100
        cum2 = (1 + returns2.pct_change()).cumprod() * 100

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=cum1.index,
            y=cum1.values,
            mode='lines',
            name=label1,
            line=dict(color='green', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=cum2.index,
            y=cum2.values,
            mode='lines',
            name=label2,
            line=dict(color='blue', width=2)
        ))

        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Cumulative Return',
            width=1200,
            height=600,
            template=self.theme
        )

        fig.show()
        logger.info("✓ Equity curves plotted")

    
    def plot_efficient_frontier(
        self,
        optimization_history: pd.DataFrame,
        risk_metric: str = 'max_drawdown',
        return_metric: str = 'sharpe_ratio',
        title: str = "Efficient Frontier"
    ):
        
        data = optimization_history.copy()
        
        # Create scatter plot
        fig = px.scatter(
            data,
            x=risk_metric,
            y=return_metric,
            color=return_metric,
            size=np.abs(data[risk_metric]),
            hover_data=['params'],
            title=title,
            labels={
                risk_metric: f"Risk ({risk_metric})",
                return_metric: f"Return ({return_metric})"
            }
        )
        
        fig.update_layout(
            width=1000,
            height=700,
            template=self.theme,
            font=dict(size=12)
        )
        
        fig.show()
        logger.info(f"✓ Efficient frontier plotted")
    
    def plot_equity_curves(
        self,
        in_sample_returns: pd.Series,
        out_sample_returns: pd.Series,
        title: str = "In-Sample vs Out-of-Sample Equity Curves"
    ):
        
        # Normalize to 100
        is_cumulative = (1 + in_sample_returns.pct_change()).cumprod() * 100
        os_cumulative = (1 + out_sample_returns.pct_change()).cumprod() * 100
        
        # Plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=is_cumulative.index,
            y=is_cumulative.values,
            mode='lines',
            name='In-Sample',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=os_cumulative.index,
            y=os_cumulative.values,
            mode='lines',
            name='Out-of-Sample',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Cumulative Return (Starting = 100)',
            width=1200,
            height=600,
            template=self.theme,
            hovermode='x unified'
        )
        
        fig.show()
        logger.info(f"✓ Equity curves plotted")
    
    def plot_monthly_returns(
        self,
        returns: pd.Series,
        title: str = "Monthly Returns Heatmap"
    ):
        
        returns_monthly = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
        
        # Pivot to calendar format
        returns_monthly.index = pd.to_datetime(returns_monthly.index)
        returns_pivot = returns_monthly.groupby([returns_monthly.index.year, returns_monthly.index.month]).mean().unstack()
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(
            returns_pivot,
            annot=True,
            fmt='.2%',
            cmap='RdYlGn',
            center=0,
            cbar_kws={'label': 'Monthly Return'},
            ax=ax
        )
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Year', fontsize=12)
        
        plt.tight_layout()
        plt.show()
        logger.info(f"✓ Monthly returns heatmap created")
    
    def plot_drawdown(
        self,
        returns: pd.Series,
        title: str = "Drawdown Over Time"
    ):
        
        cumulative = (1 + returns.pct_change()).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=drawdown.index,
            y=drawdown.values * 100,
            fill='tozeroy',
            name='Drawdown',
            line=dict(color='red'),
            fillcolor='rgba(255,0,0,0.3)'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Drawdown (%)',
            width=1200,
            height=600,
            template=self.theme
        )
        
        fig.show()
        logger.info(f"✓ Drawdown chart created")
    
    def plot_optimization_progress(
        self,
        optimization_history: pd.DataFrame,
        metric: str = 'score',
        title: str = "Optimization Progress"
    ):
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            y=optimization_history[metric],
            mode='markers+lines',
            name='Score',
            marker=dict(size=6, color=optimization_history[metric], colorscale='Viridis'),
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Iteration',
            yaxis_title=metric,
            width=1000,
            height=600,
            template=self.theme
        )
        
        fig.show()
        logger.info(f"✓ Optimization progress plotted")
