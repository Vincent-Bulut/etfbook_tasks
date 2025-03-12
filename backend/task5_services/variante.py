# correlations = {}
# for etf in tickers:
#     etf_data = final_df[final_df['ETF_Symbol'] == etf]
#
#     x = etf_data['Closing_Price'].values
#     y = etf_data['Trade_Volume'].values
#
#     mean_x = np.mean(x)
#     mean_y = np.mean(y)
#
#     numerator = np.sum((x - mean_x) * (y - mean_y))
#     denominator = np.sqrt(np.sum((x - mean_x) ** 2) * np.sum((y - mean_y) ** 2))
#
#     correlation = numerator / denominator if denominator != 0 else np.nan
#     correlations[etf] = correlation
#
# print("Pearson Correlation Coefficients:")
# for etf, corr in correlations.items():
#     print(f"{etf}: {corr:.4f}")
#
# correlation_df = pd.DataFrame({
#     'ETF_Symbol': correlations.keys(),
#     'Correlation_Coefficient': correlations.values()
# })
#
# print(correlation_df)