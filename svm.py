import numpy as np
import pandas as pd
import time
import datetime as dt
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn import svm, metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals.joblib import dump, load
from datautils import getTrainSet, getTestSet


#data is already falttened
train_data,train_labels = getTrainSet()
print("Training Data Info")
print("Training Data Shape:", train_data.shape)
print("Training Data Labels Shape:", train_labels.shape)
labels=train_labels.argmax(axis=1)
print("labels reshape :",labels)
#normalize our training data to be between 0 and 1
scaler = MinMaxScaler().fit(train_data)  
scaled_train_data=scaler.transform(train_data)
print("scaled train data",scaled_train_data)

#start model 
# C : float, optional (default=1.0) - Penalty parameter C of the error term.
#gamma : float, optional (default=’auto’) - Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’.
start_time = dt.datetime.now()
print('Start learning at {}'.format(str(start_time)))

param_C = 5
param_gamma = 0.05
classifier = svm.SVC(C=param_C,gamma=param_gamma)
classifier.fit(scaled_train_data,labels)

end_time = dt.datetime.now() 
print('Stop learning {}'.format(str(end_time)))
elapsed_time= end_time - start_time
print('Elapsed learning {}'.format(str(elapsed_time)))

## THIS TO TEST
test_data,test_labels = getTestSet()
expected = test_labels
scaled_test_data=scaler.transform(test_data)
predicted = classifier.predict(scaled_test_data)
#show_some_digits(X_test,predicted,title_text="Predicted {}")

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
      
cm = metrics.confusion_matrix(expected, predicted)
print("Confusion matrix:\n%s" % cm)

plot_confusion_matrix(cm)
print("Accuracy={}".format(metrics.accuracy_score(expected, predicted)))



#predictions = model.predict(X_test)
#from sklearn.metrics import classification_report
#print(classification_report(y_test, predictions,target_names=["blue", "red"]))






# hyperparameter grid search

