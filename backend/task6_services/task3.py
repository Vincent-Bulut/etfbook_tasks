
import json
from datetime import datetime
import pandas as pd
import yfinance as yf
import sys

if __name__ == '__main__':

    with open('portfolio_configuration.json', "r") as json_file:
        loaded_weights = json.load(json_file)

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = '2024-12-31'

    returns_data = []
    for etf, weight in loaded_weights.items():
        df = yf.download(etf, start=start_date, end=end_date, progress=False)
        df['Return'] = df['Close'].pct_change()  # Calculer les rendements journaliers
        df = df[['Return']].dropna().T  # Transposer pour obtenir une ligne par ETF

        df.insert(0, "ETF_Symbol", etf)
        df.insert(1, "Weight", weight)

        returns_data.append(df)

    returns_df = pd.concat(returns_data).reset_index(drop=True)

    returns_df.columns = ['ETF_Symbol', 'Weight'] + [f"Return_{date}" for date in returns_df.columns[2:]]

    date_columns = [col for col in returns_df.columns[2:] if col.startswith("Return_")]

    portfolio_returns = {
        "date": [col.replace("Return_", "") for col in date_columns],
        "portfolio_return": [
            (returns_df["Weight"] * returns_df[col]).sum() for col in date_columns
        ],
    }

    daily_ptf_returns = pd.DataFrame(portfolio_returns)
    daily_ptf_returns.to_excel('ETF Portfolio Returns.xlsx', index=False)

    portfolio_initial_aum = 1E6

    returns_df.set_index("ETF_Symbol", inplace=True)

    holdings = (returns_df["Weight"] * portfolio_initial_aum)

    records = []

    for day in returns_df.columns[1:]:
        returns = returns_df[day]
        new_holdings = holdings * (1 + returns)
        new_portfolio_value = new_holdings.sum()

        target_holdings = returns_df["Weight"] * new_portfolio_value
        rebalancing = target_holdings - new_holdings

        # Store daily breakdown
        for ticker in returns_df.index:
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

    df_details = pd.DataFrame(records)
    df_details.to_excel('ETF Portfolio Performance Calculation and Rebalancing.xlsx', index=False)






