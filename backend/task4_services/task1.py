
import pandas as pd

if __name__ == '__main__':
    df_etf_prices = pd.read_csv('etf_closing_prices.csv', delimiter=';')
    df_etf_trades = pd.read_csv('etf_volumes.csv', delimiter=';')


    print(df_etf_prices.head())
    print(df_etf_trades.head())

    df_merged = pd.merge(
        df_etf_prices,  # Premier DataFrame
        df_etf_trades,  # Deuxième DataFrame
        on=['date', 'etf_symbol'],  # Colonnes communes pour l'association
        how='inner'  # Méthode join : "inner" = intersection des deux DataFrames
    )

    # Afficher les premières lignes du DataFrame fusionné
    print(df_merged.head())

    df_merged['dollar_volume'] = df_merged['closing_price'] * df_merged['trade_volume']

    closing_price = df_merged['closing_price'].to_numpy()
    trade_volume = df_merged['trade_volume'].to_numpy()

    dollar_volume = closing_price * trade_volume

    df_merged['dollar_volume'] = dollar_volume

    print(df_merged)

