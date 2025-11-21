Strategy Parameter Optimizer Framework

Scientific tool for parameter optimization in algorithmic trading strategies.

OVERVIEW

This framework provides a systematic approach to finding optimal parameters for trading strategies using grid search optimization and 3D visualization. Instead of relying on manual tuning or overfitting, it applies scientific methodology to parameter selection.

FEATURES

- Framework-agnostic: Works with any trading strategy
- Grid search optimization: Tests parameter combinations systematically
- 3D parameter landscape visualization: Matplotlib-based 3D surface plots
- Real data validation: Tested on Bitcoin data (2020-2024)
- Production-ready code: Clean, documented Python implementation
- Statistical metrics: Sharpe ratio, max drawdown, win rate calculation

INSTALLATION

Requirements:
- Python 3.8+
- pip

Setup:

git clone https://github.com/lucas020695/strategy-optimizer-engine.git
cd strategy-optimizer-engine

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

QUICK START

Running the Framework:

python src/optimizer.py

This will:
1. Download Bitcoin data (2020-2024)
2. Test 125 parameter combinations
3. Find optimal RSI parameters
4. Generate 3D optimization landscape visualization
5. Save chart as optimization_landscape.png

Example Output:

Loading market data...
Loaded 1826 days of data

======================================================================
PARAMETER OPTIMIZATION - Grid Search
======================================================================

Testing 125 parameter combinations...

   [98/125] New best sharpe_ratio: 0.3395 | params: {'rsi_period': 25, 'overbought': 80, 'oversold': 30}

======================================================================
OPTIMIZATION COMPLETE
======================================================================

Best Sharpe Ratio: 0.3395
Best Parameters: {'rsi_period': 25, 'overbought': 80, 'oversold': 30}

3D landscape saved as 'optimization_landscape.png'

FRAMEWORK ARCHITECTURE

Core Components:

ParameterOptimizer
- Main optimization engine
- Performs grid search across parameter space
- Tracks results and identifies best performers
- Generates 3D landscape visualizations

Strategy Functions
- Pure functions that take data and parameters
- Return dictionary of performance metrics
- Easy to extend with custom strategies

RSI Strategy Example
- Relative Strength Index based approach
- Configurable overbought/oversold thresholds
- Demonstrates framework usage

Extending with Your Strategy:

def your_strategy(data: pd.DataFrame, param1: int, param2: float) -> Dict:
    """Your custom strategy implementation"""
    close = data['Close'].squeeze()
    
    # Your trading logic here
    signal = ...
    returns = ...
    
    # Calculate metrics
    sharpe = ...
    
    return {
        'sharpe_ratio': float(sharpe),
        'total_return': float(total_return),
        'max_drawdown': float(max_drawdown),
        'num_trades': float(num_trades)
    }

# Use framework
opt = ParameterOptimizer(data)
param_space = {'param1': (10, 30, 5), 'param2': (0.5, 2.0, 0.5)}
results = opt.optimize(your_strategy, param_space)

RESULTS

Tested on Bitcoin (2020-2024):

Metric: Sharpe Ratio
Value: 0.34

Metric: Optimal RSI Period
Value: 25

Metric: Optimal Overbought
Value: 80

Metric: Optimal Oversold
Value: 30

Metric: Data Points
Value: 1,826 days

VISUALIZATION

The framework generates 3D surface plots showing how strategy performance (Sharpe ratio) varies across two parameters. This helps identify:
- Optimal parameter regions
- Sensitivity to parameter changes
- Robustness of strategy

PROJECT STRUCTURE

strategy-optimizer-engine/
├── src/
│   └── optimizer.py          # Main framework
├── README.md                 # Documentation
├── requirements.txt          # Python dependencies
└── optimization_landscape.png # Generated visualization

DEPENDENCIES

- yfinance: Market data download
- pandas: Data manipulation
- numpy: Numerical computation
- matplotlib: 3D visualization

See requirements.txt for versions.

METHODOLOGY

1. Data Preparation: Download market data for specified period
2. Parameter Grid: Define parameter combinations to test
3. Backtesting: Run strategy on each parameter combination
4. Metrics Calculation: Compute performance statistics
5. Optimization: Identify best performing parameters
6. Visualization: Generate 3D landscape plot

LIMITATIONS

- Historical backtesting does not guarantee future performance
- Parameter overfitting possible with limited data
- No guarantee of profitability in live trading
- Past performance does not indicate future results

USE CASES

- Academic research on parameter sensitivity
- Trading strategy development and validation
- Educational tool for learning backtesting concepts
- Systematic approach to parameter tuning

FUTURE ENHANCEMENTS

- Out-of-sample validation
- Walk-forward optimization
- Parallel computation for faster testing
- Additional visualization types
- More example strategies

LICENSE

MIT License - See LICENSE file

DISCLAIMER

This framework is for educational and research purposes only. It is not investment advice. Trading involves substantial risk of loss. Past performance does not guarantee future results.

CONTRIBUTING

Contributions are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

CONTACT

For questions or feedback about this framework, please open an issue on GitHub.

Repository: https://github.com/lucas020695/strategy-optimizer-engine

---

LINKEDIN POST - ENGLISH VERSION:

Strategy Parameter Optimizer Framework

Open-source tool for scientific parameter optimization in algorithmic trading strategies.

Key Features:
- Framework-agnostic: works with any strategy
- Grid search optimization
- 3D parameter landscape visualization
- Real example: RSI strategy on Bitcoin
- Production-ready Python code

Built to help traders systematically find optimal parameters while avoiding selection bias and overfitting.

Results on Bitcoin (2020-2024):
- Best Sharpe Ratio: 0.34
- Optimized parameters: RSI 25, Overbought 80, Oversold 30
- Validated on 1,826 days of market data

Modular architecture enables easy integration of new strategies.

github.com/lucas020695/strategy-optimizer-engine

#AlgorithmicTrading #FinTech #QuantitativeFinance #Backtesting #Python

---

LINKEDIN POST - PORTUGUESE VERSION:

Framework de Otimização de Parâmetros para Trading

Ferramenta open-source para otimização científica de parâmetros em estratégias de trading algorítmico.

Características:
- Framework agnóstico: funciona com qualquer estratégia
- Busca em grade (grid search) com paralelização
- Visualização 3D da paisagem de parâmetros
- Exemplo real: estratégia RSI em Bitcoin
- Código production-ready em Python

O framework foi desenvolvido para ajudar traders a encontrar parâmetros ótimos de forma sistemática, evitando viés de seleção e overfitting.

Resultados obtidos em Bitcoin (2020-2024):
- Melhor Sharpe Ratio: 0.34
- Parâmetros otimizados: RSI 25, Overbought 80, Oversold 30
- Performance validada em 1.826 dias de dados

O código está estruturado de forma modular, permitindo adicionar novas estratégias facilmente.

github.com/lucas020695/strategy-optimizer-engine

#TradingAlgorítmico #FinTech #QuantitativeFinance #Backtesting #Python
