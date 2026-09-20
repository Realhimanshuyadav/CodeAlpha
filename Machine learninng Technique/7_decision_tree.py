import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# _______________________________________________
# 1. Load Dataset
# _______________________________________________

df = pd.read_csv("1_titanic.csv")
print(df.head())


# ______________________________________________
# 2. Select Features
# ______________________________________________

features = ['Pclass', 'Gender', 'Age', 'Sibs', 'Parch', 'Fare', 'Embarked']

X = df[features].copy()
y = df['Survived']


# _______________________________________________
# 3. Handle Missing Values
# _______________________________________________

X['Age'] = X['Age'].fillna(X['Age'].median())
X['Fare'] = X['Fare'].fillna(X['Fare'].median())
X['Embarked'] = X['Embarked'].fillna(X['Embarked'].mode()[0])


# Convert categorical variables
X = pd.get_dummies(
    X,
    columns=['Gender', 'Embarked'],
    drop_first=True
)


# _______________________________________________
# 4. Train-Test Split
# _______________________________________________

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# _______________________________________________
# 5. Hyperparameter Tuning
# _______________________________________________

depths = [1, 2, 3, 5, 10, 20]

id3_scores = []
cart_scores = []


for depth in depths:

    # __________________ ID3 __________________

    id3 = DecisionTreeClassifier(
        criterion='entropy',
        max_depth=depth,
        random_state=42
    )

    id3.fit(X_train, y_train)

    id3_pred = id3.predict(X_test)

    id3_accuracy = accuracy_score(
        y_test,
        id3_pred
    )

    id3_scores.append(id3_accuracy)


    # __________________ CART __________________

    cart = DecisionTreeClassifier(
        criterion='gini',
        max_depth=depth,
        random_state=42
    )

    cart.fit(X_train, y_train)

    cart_pred = cart.predict(X_test)

    cart_accuracy = accuracy_score(
        y_test,
        cart_pred
    )

    cart_scores.append(cart_accuracy)


# _______________________________________________
# 6. Display Result
# _______________________________________________

print("\nHyperparameter Tuning Results")

for i in range(len(depths)):

    print("\nMax Depth:", depths[i])

    print(
        "ID3 Accuracy:",
        round(id3_scores[i], 3)
    )

    print(
        "CART Accuracy:",
        round(cart_scores[i], 3)
    )


# _______________________________________________
# 7. Find Best Result
# _______________________________________________

best_id3_index = id3_scores.index(max(id3_scores))
best_cart_index = cart_scores.index(max(cart_scores))


print("\nBest ID3 Depth:",
      depths[best_id3_index])

print("Best ID3 Accuracy:",
      round(id3_scores[best_id3_index], 3))


print("\nBest CART Depth:",
      depths[best_cart_index])

print("Best CART Accuracy:",
      round(cart_scores[best_cart_index], 3))


# _______________________________________________
# 8. Plot Result
# _______________________________________________

plt.figure(figsize=(8, 5))

plt.plot(
    depths,
    id3_scores,
    marker='o',
    label='ID3'
)

plt.plot(
    depths,
    cart_scores,
    marker='o',
    label='CART'
)

plt.xlabel("Max Depth")
plt.ylabel("Accuracy")
plt.title("ID3 vs CART - Hyperparameter Tuning")

plt.xticks(depths)
plt.legend()
plt.grid(True)

plt.show()