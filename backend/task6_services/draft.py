import pandas as pd

# Define initial portfolio and returns
data = {
    "etf_symbol": ["SPY", "QQQ", "IWM"],
    "weight": [0.5, 0.3, 0.2],
    "return_2025-01-01": [0.02, 0.015, 0.01],
    "return_2025-01-02": [0.01, 0.018, 0.012],
    "return_2025-01-03": [0.015, 0.01, 0.014]
}

df = pd.DataFrame(data)
df.set_index("etf_symbol", inplace=True)

# Initial portfolio value
initial_portfolio_value = 100000


def rebalance_portfolio(df, initial_value):
    # Initialize holdings based on initial weights
    holdings = (df["weight"] * initial_value)
    portfolio_value = initial_value

    # Store results
    records = []

    for day in df.columns[1:]:  # Loop through return columns
        returns = df[day]  # Get daily returns

        # Update ETF values
        new_holdings = holdings * (1 + returns)
        new_portfolio_value = new_holdings.sum()

        # Calculate required rebalancing
        target_holdings = df["weight"] * new_portfolio_value
        rebalancing = target_holdings - new_holdings

        # Store daily breakdown
        for ticker in df.index:
            records.append({
                "date": day,
                "etf_symbol": ticker,
                "previous_holdings": holdings[ticker],
                "new_holdings": new_holdings[ticker],
                "target_holdings": target_holdings[ticker],
                "buy/sell": rebalancing[ticker],
                "portfolio_value": new_portfolio_value
            })

        # Update holdings
        holdings = target_holdings

    return pd.DataFrame(records)


# Run rebalancing simulation
df_results = rebalance_portfolio(df, initial_portfolio_value)

print(df_results)