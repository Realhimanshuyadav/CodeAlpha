import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, chi2
import seaborn as sns
import matplotlib.pyplot as pit

df=pd.read_csv("1_titanic.csv")
print("Initial Data Shape: ",df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())

#Fill missing Age values with median
df['Age']=df['Age'].fillna(df['Age'].median())

df['Embarked']=df['Embarked'].fillna(df['Embarked'].mode()[0])

if 'Cabin' in df.columns:
    df.drop(columns=['Cabin'],inplace=True)
    
print("\nMissing Values after Handling:")
print(df.isnull().sum())

#Encoding
df['Gender']=LabelEncoder().fit_transform(df['Gender'])
df['Embarked']=LabelEncoder().fit_transform(df['Embarked'])

#Feature Scaling
scaler = StandardScaler()
df[['Age','Fare']]=scaler.fit_transform(df[['Age','Fare']])

drop_columns = ['Survived']

if 'Name' in df.columns:
    drop_columns.append('Name')

if 'Ticket' in df.columns:
    drop_columns.append('Ticket')
    
x=df.drop(columns=drop_columns)
y=df['Survived']

X_positive = abs(x)

selector = SelectKBest(score_func=chi2,k=5)
X_selected=selector.fit_transform(X_positive,y)

selected_features = x.columns[selector.get_support()]
print("\nSelected Features:")
print(selected_features)
print("\nFeature Scores:")

scores= pd.DataFrame({
    'Feature':x.columns,
    'Chi2 Score': selector.scores_
})

print(scores.sort_values(by='Chi2 Score',ascending=False))