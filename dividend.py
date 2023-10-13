import investpy
import pandas as pd
# from 2013 to 2023
years = [str(i) for i in range(2013, 2024)]
tickers = investpy.stocks.get_stocks_list(country='mauritius')
#sort tickers in alphabetical order
tickers.sort()
# create a dataframe with columns ticker and years with dividend value
df = pd.DataFrame(columns=['Ticker'] + years)

def get_dividend(stock):
    df = investpy.get_stock_dividends(stock, country='mauritius')
    #sort by ascending date
    df = df.sort_values(by='Date', ascending=True)
    # combine rows with same year in Date column by adding the dividend value
    dividend_year = df.groupby(pd.to_datetime(df['Date']).dt.year)['Dividend'].sum().reset_index()
    dividend_year.columns = ['Year', 'Dividend']
    dividend_year.set_index('Year', inplace=True)
    return dividend_year



# # fill the dataframe with dividend values
for i in range(len(tickers)):
    try:
        print('Getting dividend for', tickers[i])
        div = get_dividend(tickers[i])
        df.loc[i] = [tickers[i]] + [div.Dividend.get(x,0) for x in range(2013,2024)]
    except Exception as e:
        print('Error getting dividend for', tickers[i], e)
        df.loc[i] = [tickers[i]+' - '+str(e)] + [0 for x in range(2013,2024)]

df.to_csv('dividend.csv', index=False)

