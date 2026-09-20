import pandas as pd 
import numpy  as pn 
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("1_titanic.csv")

print("Shape of dataset: ", df.shape)
print("\nFirst 5 row ")
print(df.head())

print("\nDataset information")
print(df.info())
print("\nSatatistical Summary")
print(df.describe())
print("\nMissing values")
print(df.isnull().sum())

print("\nSurvived count")
print(df['Survived'].value_counts())

sns.countplot(x='Survived', data=df)
plt.title("Survived count")
plt.show()

print("\nGender Distribution")
print(df['Gender'].value_counts())
sns.countplot(x='Gender',hue='Survived',data=df)
plt.title("Gender vs Survival")
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df['Age'], bins=20, kde=True)
plt.title("Age Distribution ")
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df['Fare'],bins=20,kde=True)
plt.title("Fare Distribution")
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(x=df['Age'])
plt.title("Boxplot of age ")
plt.show()

# Step 10: Correlation Analysis
numeric_df=df.select_dtypes(include=['number'])
correlation_matrix=numeric_df.corr()
plt.figure(figsize=(10,6))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='coolwarm',
    linewidths=0.5
)
plt.title("Features Correlation Heatmap")
plt.show()