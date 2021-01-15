import csv
import numpy as np
from sklearn.tree import DecisionTreeClassifier
# for saving machine learning model
import pickle
# confusion matrix for testing
#from sklearn.metrics import confusion_matrix 

x_train = [] # Make an empty list to hold file rows

# Read file rows and append them to list
with open ("Data/Questions.txt", 'rt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x_train.append(row)

# Cast list to numpy array
x_train = np.array(x_train, dtype = np.uint8)

# Hot-encode variable names to either 0 or 1
length = len(x_train)
for index in range(length):
    for iterator in range(9):
        if x_train[index][iterator][0] == "!":
            x_train[index][iterator] = 0
        else:
            x_train[index][iterator] = 1

y_train = [] # Make an empty list to hold file rows

# Read file rows and append them to list
with open ("Data/Responses_striped.txt", 'rt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        y_train.append(row)

# Cast list to numpy array
y_train = np.array(y_train, dtype = np.uint8)

# Make a classifier 
classifier = DecisionTreeClassifier(criterion = "entropy")
classifier.fit(X = x_train, y = y_train)

with open ("DT_model.pkl", 'wb') as file:
    pickle.dump(classifier, file)
    

# For testing purposes
"""
y_predict = classifier.predict(x_train)
Matrix = confusion_matrix(y_train, y_predict)
"""
