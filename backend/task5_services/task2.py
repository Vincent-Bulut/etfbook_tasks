import pandas as pd
import yfinance as yf

from datetime import datetime

if __name__ == '__main__':
    tickers = ['SPY', 'QQQ']

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = '2025-01-01'

    data_frames = []
    for etf in tickers:
        df = yf.download(etf, start=start_date, end=end_date, progress=False)
        df['ETF_Symbol'] = etf
        df = df[['ETF_Symbol', 'Close', 'Volume']].reset_index()
        df.columns = ['Date', 'ETF_Symbol', 'Closing_Price', 'Trade_Volume']
        data_frames.append(df)

    final_df = pd.concat(data_frames).sort_values(by=['Date', 'ETF_Symbol']).reset_index(drop=True)

    print(final_df)

    correlations = {}
    for etf in tickers:
        etf_data = final_df[final_df['ETF_Symbol'] == etf]
        correlation = etf_data['Closing_Price'].corr(etf_data['Trade_Volume'])
        correlations[etf] = correlation

    print("Pearson Correlation Coefficients:")
    for etf, corr in correlations.items():
        print(f"{etf}: {corr:.4f}")

    correlation_df = pd.DataFrame({
        'ETF_Symbol': correlations.keys(),
        'Correlation_Coefficient': correlations.values()
    })

    print(correlation_df)