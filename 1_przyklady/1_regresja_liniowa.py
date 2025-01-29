import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

df = pd.read_csv('weight-height.csv', delimiter=';', comment='#')
print(df)
print(type(df))

print(df.head(3))   # wyświetl 3 pierwsze wiersze
print(f'\nzliczanie wartosci kolumny Gender\n{df.Gender.value_counts()}')

#zmiana jednostek
df.Height *= 2.54
df.Weight /= 2.2
print(df.head(3))

# wykresy
plt.hist(df.Weight)
plt.show()

sns.histplot(df.query("Gender=='Male'").Weight)
sns.histplot(df.query("Gender=='Female'").Weight)
plt.show()

# zamiana gender na dane numeryczne
df = pd.get_dummies(df)
print(df)

# usuwam kolumnę "Gender_Male
del (df['Gender_Male'])
# zostaje kolumna Gender_Female, zmieniamy nazwę
df = df.rename(columns={'Gender_Female': 'Gender'})
# False - to facet,   True - Kobieta
print(df)

model = LinearRegression()
model.fit(df[['Height', 'Gender']]  ,   df['Weight'])  #dane wejściowe i wyjściowe
print(f'Wspolczynnik kierunkowy: {model.coef_}\nWyraz wolny: {model.intercept_}')

print(f'Weight = Height * {model.coef_[0]} + Gender * {model.coef_[1]} + {model.intercept_}')

#sprawdźmy coś
print(model.predict([[160, 0]]))   #ile waży człowiek 160cm wzostu, kobieta
print(model.predict([[160, 0], [179, 1], [146, 1]]))