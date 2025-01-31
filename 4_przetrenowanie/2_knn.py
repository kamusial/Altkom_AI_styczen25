import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("iris.csv")
#nie można df.class
print(df["class"].value_counts())
#class - zmienn wynikowa, powinna mieć harakter numeryczny.
species = {
    "Iris-setosa":0, "Iris-versicolor":1, "Iris-virginica":2
}
df["class_value"] = df["class"].map(species)
print(df["class_value"].value_counts())

sample = np.array([5.6, 3.2, 5.2, 1.45])

sns.scatterplot(data=df, x='sepallength', y='sepalwidth', hue='class')
plt.scatter(5.6 , 3.2, c="r")
plt.show()

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
X = df.iloc[:, :4]
y = df.class_value
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)
model = KNeighborsClassifier(5)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
print(pd.DataFrame( confusion_matrix(y_test, model.predict(X_test)  ) ))

import joblib
joblib.dump(model, "knn.model")

model1 = joblib.load("knn.model")
print(dir(model1))
print(model1.classes_)
print(model1.n_neighbors)
print(model1.predict(sample.reshape(1,-1)))