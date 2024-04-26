import pandas
import pickle
from sklearn import preprocessing

#hier sind daten f. alle 4000 aktien sowie den index enthalten
data = pandas.read_csv('D:/Bibliotheken/docxxx/UNI/htw/SS24/aki/code/test/paper_mutli_lstm/stocks.csv')

time = min(data.Date)
end = max(data.Date)
#end = 253

T = 20

while time < end - T:
    print(time)
    subset = data[ (data['Date'] >= time) & (data['Date'] < time + T + 1)]
    #aktien, die zum zeitpunkt am leben waren
    table = pandas.pivot_table(subset, index=['Date'], columns=['Ticker'])
    table.columns = table.columns.get_level_values(1)
    table = table.dropna(axis=1)
    table = table.loc[:,table.nunique()!=1]

    #normalize
    x = table.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    table = pandas.DataFrame(x_scaled, columns=table.columns)

    targets = table.iloc[T]
    table = table[0:T]
    correlations = table.corr()
    correlations = correlations.dropna(axis=1)
    for col in correlations.columns:
        item = dict()
        item['y'] = targets[col]
        item['Y'] = table[col]
        pos_stocks = list(correlations[col].nlargest(21).index) # largest correlation is with stock itself
        pos_stocks.remove(col)
        item['X_p'] = table[pos_stocks]
        neg_stocks = list(correlations[col].nsmallest(20).index)
        item['X_n'] = table[neg_stocks]
        with open('c:/data/htw/2021_SS/AKI/Samples/' + col + '_' + str(time) + '.pkl', 'wb') as f:
            pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)
    time = time + 1
