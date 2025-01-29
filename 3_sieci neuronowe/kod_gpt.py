import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def load_data(filename):
    # Wczytanie danych z pliku CSV
    data = pd.read_csv(filename)

    # Zakładamy, że pierwsza kolumna to Celsius, druga to Fahrenheit
    X = data.iloc[:, 2].values  # Temperatury w Celsjuszach
    y = data.iloc[:, 1].values  # Temperatury w Fahrenheicie

    return X, y

def build_and_train_model(X, y):
    # Budowanie modelu
    model = Sequential([
        Dense(64, activation='relu', input_shape=(1,)),
        Dense(64, activation='relu'),
        Dense(1)
    ])

    # Kompilacja modelu
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Trenowanie modelu na wszystkich dostępnych danych
    model.fit(X, y, epochs=50, batch_size=32, verbose=1)

    return model

def evaluate_and_plot(model, X, y):
    # Ocena modelu na tych samych danych
    loss = model.evaluate(X, y, verbose=0)
    print(f'Model loss: {loss:.4f}')

    # Wykres liniowy przewidywań modelu
    plt.figure(figsize=(10, 5))
    plt.scatter(X, y, color='blue', label='Actual Data')
    predictions = model.predict(X)
    plt.plot(X, predictions, color='red', label='Model Predictions')
    plt.title('Comparison of Actual Data and Model Predictions')
    plt.xlabel('Degrees Celsius')
    plt.ylabel('Degrees Fahrenheit')
    plt.legend()
    plt.show()

def main():
    filename = 'f-c.csv'  # Nazwa pliku CSV, który musi znajdować się w katalogu roboczym

    X, y = load_data(filename)
    model = build_and_train_model(X, y)
    evaluate_and_plot(model, X, y)

if __name__ == '__main__':
    main()
