import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# _______________________________________________________________
# 1. Load Dataset
# _______________________________________________________________

df = pd.read_csv("1_titanic.csv")

print("First 5 rows of dataset:")
print(df.head())


# _______________________________________________________________
# 2. Select Features
# _______________________________________________________________

features = [
    'Pclass',
    'Gender',
    'Age',
    'SibSp',
    'Parch',
    'Fare',
    'Embarked'
]

X = df[features].copy()
y = df['Survived']


# _______________________________________________________________
# 3. Handle Missing Values
# _______________________________________________________________

X['Age'] = X['Age'].fillna(X['Age'].median())

X['Fare'] = X['Fare'].fillna(X['Fare'].median())

X['Embarked'] = X['Embarked'].fillna(
    X['Embarked'].mode()[0]
)


# _______________________________________________________________
# 4. Convert Categorical Variables
# _______________________________________________________________

X = pd.get_dummies(
    X,
    columns=['Gender', 'Embarked'],
    drop_first=True
)


# _______________________________________________________________
# 5. Sensitivity Analysis
# _______________________________________________________________

test_sizes = [0.1, 0.2, 0.3, 0.4]

dt_scores = []
rf_scores = []


for test_size in test_sizes:

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
        stratify=y
    )


    # -----------------------------------------------------------
    # Decision Tree
    # -----------------------------------------------------------

    dt = DecisionTreeClassifier(
        max_depth=5,
        random_state=42
    )

    dt.fit(X_train, y_train)

    dt_pred = dt.predict(X_test)

    dt_accuracy = accuracy_score(
        y_test,
        dt_pred
    )

    dt_scores.append(dt_accuracy)


    # -----------------------------------------------------------
    # Random Forest
    # -----------------------------------------------------------

    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    rf.fit(X_train, y_train)

    rf_pred = rf.predict(X_test)

    rf_accuracy = accuracy_score(
        y_test,
        rf_pred
    )

    rf_scores.append(rf_accuracy)


# _______________________________________________________________
# 6. Display Results
# _______________________________________________________________

print("\n")
print("==========================================")
print("      SENSITIVITY ANALYSIS RESULTS")
print("==========================================")


for i in range(len(test_sizes)):

    train_percentage = int(
        (1 - test_sizes[i]) * 100
    )

    test_percentage = int(
        test_sizes[i] * 100
    )

    print("\nTrain-Test Split:",
          str(train_percentage) + ":" +
          str(test_percentage))

    print(
        "Decision Tree Accuracy:",
        round(dt_scores[i], 3)
    )

    print(
        "Random Forest Accuracy:",
        round(rf_scores[i], 3)
    )


# _______________________________________________________________
# 7. Plot Results
# _______________________________________________________________

split_names = [
    '90:10',
    '80:20',
    '70:30',
    '60:40'
]


plt.figure(figsize=(8, 5))


plt.plot(
    split_names,
    dt_scores,
    marker='o',
    label='Decision Tree'
)


plt.plot(
    split_names,
    rf_scores,
    marker='o',
    label='Random Forest'
)


plt.xlabel("Train-Test Split Ratio")

plt.ylabel("Accuracy")

plt.title("Sensitivity Analysis")

plt.legend()

plt.grid(True)

plt.show()