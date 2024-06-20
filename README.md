# Portfolio Management using Reinforcement Learning

## Problem Setup
Effective portfolio management is crucial in finance for maximizing returns and managing risks.
Traditional methods often struggle in fast-changing markets, leading to suboptimal asset allocation and limited
diversification. This project addresses these issues by employing reinforcement learning, a dynamic strategy
that adapts to real-time market data. Unlike conventional approaches, reinforcement learning optimizes asset
allocation systematically by balancing exploration (testing new strategies) with exploitation (capitalizing on
known strategies). This method enhances the discovery and refinement of investment strategies, potentially
leading to superior returns. The project aims to deepen our understanding of applying reinforcement learning in
real-world financial contexts, enhancing investment strategy agility and efficacy.

## Methodology
To optimize portfolio management, we implemented a deep reinforcement learning algorithm tailored to the
financial market. This approach allowed us to dynamically adjust asset allocations based on predicted rewards
and optimize the overall portfolio performance. Below is the detailed methodology used:

### Environment Configuration
We developed a simulated single stock trading environment compatible with OpenAI Gym to train and evaluate
RL agents. This environment simulates stock market conditions where agents make decisions about portfolio
allocations.

### State Space
In our effort to augment the RL agent's grasp of market dynamics, we integrated several key technical indicators
alongside the covariance matrix for each stock ticker. These indicators, including Moving Average Convergence
Divergence (MACD), Bollinger Bands (BB), Relative Strength Index (RSI), Accumulation/Distribution Line
(ADL), and Ichimoku Cloud, are derived from historical price and volume data. Together, they provide valuable
insights into market trends and potential buy or sell signals, enhancing the RL agent's decision-making
capabilities.
The covariance matrix is computed using daily returns from closing prices, expressed as percentage changes
day-to-day. Using a 252-day rolling window, we calculate the covariance between stock returns, helping assess
asset risk and overall portfolio diversification.

### Action Space:
The action space defines all possible portfolio allocations. Each action determines capital allocation among
stocks. The size of the action space corresponds to the number of unique stocks, allowing the agent to make
strategic capital distribution decisions during trading.

### Environment Workflow
Initialization: Starts with input data, stock details, transaction costs, and reward scaling.
Action Selection: At each step, the RL agent picks actions for portfolio allocation. The environment then
calculates portfolio return, updates state, and computes rewards.
Termination: Episodes end when reaching a set limit, like maximum trading days. Cumulative rewards and
metrics like Sharpe ratio are generated.
Reset: The environment resets after each trading episode.

## Learning Algorithm
The Advantage Actor-Critic (A2C) algorithm is a reinforcement learning method integrating policy-based and
value-based strategies for optimal policy learning in sequential decision tasks. A2C consists of:
1. Actor Network (Policy Network): Models the policy by mapping states to actions, outputting a probability
distribution across the action space. Updates are driven by the advantage function , assessing the benefit
of specific actions over the average.
2. Critic Network (Value Network): Assesses state-action pairs by predicting their expected returns to
approximate the value function , representing expected cumulative rewards from a given state under a
policy. It stabilizes updates by providing a reference for the advantages calculated by the actor network.
Advantage Estimation: Defined as the difference between the estimated value of an action and the
current state value , guiding the actor network's updates to enhance long-term rewards.
Policy Gradient Updates: Both networks update using gradients derived from the advantage function. For the
actor: , and for the critic: .
Here, and are the learning rates for the actor and critic networks, respectively, optimized through
stochastic gradient ascent to maximize expected returns.


## Background
Reinforcement learning algorithms like Q-learning, Policy Iteration, and A2C have demonstrated
success in various domains, from gaming to finance. Unlike supervised or unsupervised learning, reinforcement
learning learns optimal behavior through trial and error, with the agent interacting with its environment and
receiving rewards. This process mimics human learning, making it suitable for dynamic environments like
finance. In this project, we explore using A2C, a reinforcement learning algorithm, for portfolio optimization,
aiming to improve investment strategy effectiveness. Through this work, we aim to deepen our understanding of
applying reinforcement learning in finance, potentially enhancing investment strategy agility and efficacy.

## Initial Code
Our portfolio management project begins with three main scripts: data_scraping.py, data_cleaning.py,
data_preprocessing.py, and a Jupyter notebook, Main.ipynb. These components form the foundation of our
machine learning model for managing financial portfolios with reinforcement learning.
Data Scraping: We use yfinance in data_scraping.py to download historical stock data, including daily prices
and volumes. The data is compiled into a CSV file after merging data frames from various stock tickers.
Data Cleaning: The data_cleaning.py script processes this stock data by removing incomplete records and
ensuring that only stocks with reliable historical data are used. It also standardizes the time frame for all stocks,
ensuring consistency across the dataset.
Data Preprocessing: In data_preprocessing.py, we calculate key technical indicators like MACD, Bollinger
Bands, RSI, ADL, and Ichimoku Cloud. We also compute a covariance matrix for the stocks, which helps in
understanding price movements and correlations.
Model Implementation: Main.ipynb incorporates this preprocessed data into a trading environment in OpenAI
Gym, where we train a reinforcement learning model using the Advantage Actor-Critic (A2C) method. This
notebook manages the complete workflow from data handling to the final model training and evaluation,
focusing on optimal asset allocation and considering transaction costs.
These initial stages leverage Python libraries such as pandas, numpy, and matplotlib for data handling and
analysis, which are essential for applying reinforcement learning effectively in portfolio management.

## Python Optimization
In our Reinforcement Learning project for Portfolio Management, we focused on optimizing Python
code to improve its speed and efficiency, critical for managing complex financial calculations. One key
optimization strategy involved localizing global variables used for settings and data management, thereby
enhancing Python's access speed, reducing memory usage, and improving overall resource efficiency.
Additionally, we refactored data structures, transitioning from dictionaries to lists and tuples for storing data.
This shift proved advantageous for indexed operations and helped lower memory consumption, particularly
important when dealing with large datasets of stock prices and indicators.
Furthermore, we addressed performance bottlenecks by minimizing nested loops in data processing. By
leveraging list comprehensions and the map() function, we were able to enhance execution speed and code
clarity. Moreover, we streamlined the code by favoring Python's optimized built-in functions over custom
functions, thereby reducing delays associated with function calls. Additionally, we optimized conditional
statements within loops by merging conditions and removing unnecessary checks, further accelerating
execution. Through the use of the Line Profiler tool, we confirmed that these optimizations significantly
enhanced the program's responsiveness and its ability to handle real-time data effectively.

## Cython Optimization
In optimizing our portfolio management project, we utilized several Cython features to enhance code
efficiency and performance directly within our Jupyter Notebook environment. The %load_ext cython
command activates Cython, allowing us to compile code to C. With the %%cython cell magic, we specify
which sections of our code should be compiled. The --annotate option helped visualize the conversion
efficiency, showing areas needing further optimization. Performance improvements are achieved by disabling
bounds checking (@cython.boundscheck(False)), preventing negative indexing (@cython.wraparound(False)),
and enabling C-style division (@cython.cdivision(True)), which collectively speed up array operations and
arithmetic calculations by eliminating redundant safety checks. We also use cimport to integrate C-optimized
libraries and functions, such as NumPy, enhancing computational speed. Variables are declared with C static
types using cdef, reducing the overhead of Python’s dynamic typing and significantly improving runtime
performance in our computationally intensive financial calculations.

## Numba Optimization
After integrating Cython to optimize our project, we further elevated its efficiency by incorporating
Numba, a crucial tool for rapidly processing intricate tasks within financial markets. Numba's Just-In-Time
(JIT) compiler seamlessly integrated into our environment, where we utilized its `@jit` decorator to enhance
key functions responsible for computing financial indicators and executing trades. By leveraging Numba's
capabilities, we transformed these functions into efficient machine code, significantly improving their
performance. Through strategic implementation of parameters such as `nopython=True` and specifying
input/output types, we minimized overhead associated with dynamic typing, further enhancing computational
efficiency. As a result, the execution time of critical computations was notably reduced from 819 seconds to
approximately 627 seconds, substantially accelerating both data processing and trade execution.
This optimization not only bolstered the project's speed but also ensured its consistency and reliability,
particularly crucial amidst the ever-fluctuating conditions of financial markets. The integration of Numba
empowered our system to maintain stable and efficient decision-making processes, even in the face of dynamic
market environments. Ultimately, these enhancements underscore the project's adaptability and responsiveness,
positioning it to navigate the complexities of financial landscapes with increased agility and effectiveness.

## Multiprocessing & Multithreading Optimization
After achieving enhancements with Numba, we further elevated our project by integrating
multiprocessing and multithreading techniques to enhance performance, crucial for managing vast data and
ensuring swift calculations in financial portfolio management. Utilizing Python's multiprocessing and threading
modules, we parallelized tasks across multiple CPU cores, significantly reducing overall execution time. Key
functions involved in data preprocessing and financial computations were adapted to run concurrently, ensuring
thread safety and minimizing shared state to prevent performance bottlenecks.
Tasks were categorized by nature, with computationally intensive tasks like covariance matrix
calculations employing multiprocessing for separate memory spaces, while I/O-bound tasks like data fetching
and preprocessing utilized multithreading to enhance responsiveness. This integration notably reduced the
execution time of complex computations from 627 seconds to 306 seconds, critical for optimizing asset
allocations. These techniques not only accelerated execution times but also enhanced our capacity to handle
larger datasets effectively, proving essential for real-time financial analysis in dynamic market conditions.


## Conclusion
In conclusion, our project successfully employed a series of optimization techniques to significantly
reduce both the total execution time and wall time required for our reinforcement learning-based portfolio
management system. Starting with an initial code execution time of 2386 seconds, we progressively
implemented Python optimizations, Cython, Numba, and multiprocessing/multithreading, each dramatically
enhancing performance.
Multiprocessing and Multithreading optimization was the most effective, reducing the total runtime to
12% of its original runtime. Similarly, Numba optimization was able to reduce it to 26%, Cython to 34% and
Python 46%. Multiprocessing and multithreading minimized execution time to 306 seconds and maximized
system efficiency under the demanding conditions of financial markets. This strategic use of parallel computing
significantly enhanced our system's ability to manage large datasets and perform rapid calculations, essential for
real-time decision-making.
