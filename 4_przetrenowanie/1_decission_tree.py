import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from mlxtend.plotting import plot_decision_regions

# Read and prepare data
df = pd.read_csv("iris.csv")
print("Value counts:\n", df["class"].value_counts())
print("\nDataset:\n", df)

# Create numeric class values
species = {
    "Iris-setosa": 0,
    "Iris-versicolor": 1,
    "Iris-virginica": 2
}
df["class_value"] = df["class"].map(species)

# Sepal visualization
plt.figure(figsize=(7, 7))
sns.scatterplot(data=df, x='sepallength', y='sepalwidth', hue='class')
plt.title('Sepal Length vs Width')
plt.show()

# Petal visualization
plt.figure(figsize=(7, 7))
sns.scatterplot(data=df, x='petallength', y='petalwidth', hue='class')
plt.title('Petal Length vs Width')
plt.show()

# Train decision tree
X = df[["sepallength", "sepalwidth"]]
y = df.class_value
model = DecisionTreeClassifier(max_depth=10)
model.fit(X, y)

# Plot decision regions
plt.figure(figsize=(7, 7))
plot_decision_regions(X.values, y.values, clf=model)
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.title('Decision Tree Regions')
plt.show()

# The dtreeplt visualization part seems to be using a non-standard library
# Instead, we can use scikit-learn's built-in tree visualization:
from sklearn.tree import plot_tree
plt.figure(figsize=(15, 10))
plot_tree(model, feature_names=X.columns,
          class_names=["setosa", "versicolor", "virginica"],
          filled=True)
plt.show()
