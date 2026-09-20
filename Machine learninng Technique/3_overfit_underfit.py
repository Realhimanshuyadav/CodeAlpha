import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold,cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier

# -----------------------------------
# 1. Load Dataset
# -----------------------------------

df = pd.read_csv("1_titanic.csv")

print(df.head())
print(df.shape)

# -----------------------------------
# 2. Select useful features
# -----------------------------------

features = ['Pclass', 'Gender', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

X = df[features]
y = df['Survived']

# -----------------------------------
# 3. Handle missing values
# -----------------------------------

X['Age'] = X['Age'].fillna(X['Age'].median())
X['Fare'] = X['Fare'].fillna(X['Fare'].median())
X['Embarked'] = X['Embarked'].fillna(X['Embarked'].mode()[0])

# Convert categorical variables into numbers
X = pd.get_dummies(X, columns=['Gender', 'Embarked'], drop_first=True)

print("\nFeatures after encoding:")
print(X.head())

# -----------------------------------
# 4. Train-Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------------
# 5. Compare Decision Tree Classifier with different depths
# -----------------------------------

depths = [1, 2, 3, 5, 10, 20, None]

train_scores = []
test_scores = []
cv_scores = []

for depth in depths:

    model = DecisionTreeClassifier(
        max_depth=depth,
        random_state=42
    )

    # Train model 
    model.fit(X_train, y_train)

    # Training accuracy, prediction on training set
    train_pred = model.predict(X_train)

    train_accuracy = accuracy_score(y_train, train_pred)

    # Testing accuracy
    test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_pred)
    # 5-Fold Cross Validation
    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring='accuracy'
    )

    train_scores.append(train_accuracy)
    test_scores.append(test_accuracy)
    cv_scores.append(scores.mean())

    print("\nMax Depth: ", depth)
    print("Training Accuracy: ", round(train_accuracy, 3))
    print("Testing Accuracy: ", round(test_accuracy, 3))
    print("CV Accuracy: ", round(scores.mean(), 3))
    print("CV Standard Deviation: ", round(scores.std(), 3))

# -----------------------------------
# 6. Plot Training and Testing Accuracy
# -----------------------------------

plt.figure(figsize=(10, 6))

x = range(len(depths))

plt.plot(x, train_scores, marker='o',  label='Training Accuracy')
plt.plot(x, test_scores, marker='o',  label='Testing Accuracy')
plt.plot(x, cv_scores, marker='o',  label='CV Accuracy')

plt.xticks(x, ['1', '2', '3', '5', '10', '20', 'None'])

plt.xlabel('Decision Tree Max Depth')
plt.ylabel('Accuracy')
plt.title('Decision Tree Performance')

plt.legend()
plt.grid(True)

plt.show()


# -----------------------------------------------
# 7. Find the best model using Cross Validation
# -----------------------------------------------

best_index = cv_scores.index(max(cv_scores))
best_depth = depths[best_index]

print("Depths: ", depths)
print([round(float(x), 3) for x in cv_scores])

print("\nBest Max Depth: ", best_depth)
print("Best CV Accuracy: ", round(cv_scores[best_index], 3))