#%%
import pandas as pd
from sklearn import tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('data_con_2018.csv')

# =============================================================================
# CLEADNING DATA WHICH DO NOT HAVE AMOUNT OR THROUGHPUT TIME
# =============================================================================

#print(len(df))

df.drop(df[df['Amount'] == 0].index, inplace = True)
df.drop(df[df['Throughput Time'] == 0].index, inplace = True)

#print(len(df))
#data=df.iloc[:,list(range(1,len(df.columns)-1))]
#target=df.iloc[:,-1]
#print(df.columns)
#%%
# =============================================================================
# ACCEPTED/REJECTION PREDECTION 
# =============================================================================

column_index=[1, 2, 3, 4, 5, 6, 7, 9]
data=df.iloc[:,column_index]
target=df.iloc[:,8]
#print(target)
#print(data)
X=data.to_numpy()
y=target.to_numpy()

#print(set(y))
print("ACCEPED / REJECTED PREDICTION")
print("------------------------------------------------------------------------------")
#%%
# =============================================================================
# DECISION TREE CALSSIFIER
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=90)

clf = tree.DecisionTreeClassifier()
#clf = tree.DecisionTreeRegressor()

#clf = clf.fit(X_train, y_train)
clf = clf.fit(X_train, y_train)

#INPUTING THE VALUES IN MODEL 
y_pred = clf.predict(X_test)

accuracy=accuracy_score(y_test, y_pred)
precision,recall,fscore,support = precision_recall_fscore_support(y_test, y_pred, average='micro')

print("DECISION TREE :")
# ACCURACY
print('Accuracy: %.2f',accuracy)
# PRECISION
print('Prescision: %.2f',precision)
# RECALL
print('Recall: %.2f',recall)

# The mean squared error
#print('Mean squared error: %.2f',mean_squared_error(y_test, y_pred))

# The coefficient of determination: 1 is perfect prediction
#print('Coefficient of determination: %.2f',r2_score(y_test,y_pred))

# =============================================================================
# RANDOM FOREST CLASIFIER (IMPROVED MODEL)
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

rf = RandomForestClassifier(n_estimators=100,random_state=0)

rf.fit(X_train, y_train)

#INPUTING THE VALUES IN MODEL 
y_pred = rf.predict(X_test)

accuracy=accuracy_score(y_test, y_pred)
precision,recall,fscore,support = precision_recall_fscore_support(y_test, y_pred, average='micro')

print("\nRANDOM FORESET CLASSIFIER:")
print("Accuracy on training set:.2f%",rf.score(X_train,y_train))
print("Accuracy on test set:.2f%",rf.score(X_test,y_test))
# ACCURACY
print('Accuracy: %.2f',accuracy)
# PRECISION
print('Prescision: %.2f',precision)
# RECALL
print('Recall: %.2f',recall)

# The mean squared error
#print('Mean squared error: %.2f',mean_squared_error(y_test, y_pred))

# The coefficient of determination: 1 is perfect prediction
#print('Coefficient of determination: %.2f',r2_score(y_test,y_pred))
print("------------------------------------------------------------------------------")
print("THROUGHPUT PREDICTION")
print("------------------------------------------------------------------------------")
# =============================================================================
# PREDICTING THE THRUGHPUT TIME
# =============================================================================
column_index=[1, 2, 3, 4, 5, 6, 7, 8]
#data=df.iloc[:,list(range(1,len(df.columns)-1))]
data=df.iloc[:,column_index]
target=df.iloc[:,9]
#print(target)
#print(data)
X=data.to_numpy()
y=target.to_numpy()
#%%
# =============================================================================
# REGRESSION DECISION TREE
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

#clf = tree.DecisionTreeClassifier()
clf = tree.DecisionTreeRegressor()

#clf = clf.fit(X_train, y_train)
clf = clf.fit(X_train, y_train)

#INPUTING THE VALUES IN MODEL 
y_pred = clf.predict(X_test)

print("REGRESSION DECISION TREE :")
# The mean squared error
print('Mean squared error: %.2f',mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f',r2_score(y_test,y_pred))

# =============================================================================
# RANDOM FOREST REGRESSOR (IMPROVED MODEL)
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

rf = RandomForestRegressor(n_estimators=100,random_state=0)

rf.fit(X_train, y_train)

#INPUTING THE VALUES IN MODEL 
y_pred = rf.predict(X_test)

#accuracy=accuracy_score(y_test, y_pred)
#precision,recall,fscore,support = precision_recall_fscore_support(y_test, y_pred, average='micro')

print("\nRANDOM FORESET REGRESSOR:")
# The mean squared error
print('Mean squared error: %.2f',mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f',r2_score(y_test,y_pred))

# =============================================================================
# LINERAR REGRESSION
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)


print("\nLINEAR REGRESSION :")
# The coefficients
#print('Coefficients: \n', regr.coef_)
# The mean squared error
print('Mean squared error: %.2f',mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f',r2_score(y_test,y_pred))
print("------------------------------------------------------------------------------")