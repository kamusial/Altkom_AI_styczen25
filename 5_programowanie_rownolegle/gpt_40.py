import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


def clean_data(file_path):
    """Attempt to clean data by skipping rows with inconsistent number of fields."""
    try:
        # Attempt to read the CSV with skipping bad lines
        data = pd.read_csv(file_path, comment='#')
        messagebox.showinfo("Info", "Some rows with inconsistent data were skipped.")
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clean data: {str(e)}")
        return None


def load_data(file_path):
    try:
        # Load the data, with a preliminary check for bad lines
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")

        # Check for missing values
        if data.isnull().values.any():
            messagebox.showwarning("Warning", "Missing values found in the data. Please preprocess it before training.")
            return None
        return data
    except pd.errors.ParserError as e:
        messagebox.showwarning("Parser Error", f"Error parsing data: {e}. Attempting to clean data...")
        return clean_data(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        return None


def build_and_train_model(data):
    # Assuming the last column is the target variable
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Create a simple neural network for binary classification
    model = Sequential([
        Dense(32, input_dim=X.shape[1], activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X, y, epochs=10, batch_size=10, verbose=1)
    return model


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        data = load_data(file_path)
        if data is not None:
            model = build_and_train_model(data)
            if model:
                messagebox.showinfo("Info", "Model trained successfully.")


def main():
    root = tk.Tk()
    root.title("Binary Classification with Neural Network")

    tk.Label(root, text="Select a CSV file for training:").pack()

    browse_button = tk.Button(root, text="Browse", command=browse_file)
    browse_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
