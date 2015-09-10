from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import preprocessing
from time import time
import numpy as np

t0 = time()

classifier = int(raw_input(
"""
Enter number corresponding to classifier you would like to use:
1. Support Vector Machines
2. Gaussian Naive Bayes
3. Multinomial Naive Bayes
4. Stochastic Gradient Descent with Logistic Regression loss function
"""))

dataset = int(raw_input(
"""
Enter number corresponding to data set you would like to use:
1. First half and second half
2. Alternating
3. Alternating with attack type
4. Alternating with attack type and target type
"""))

# Assign appropriate datasets
input_files = ['half', 'alternating', 'alternating-with-attacktype', 'alternating-all']
filename = input_files[dataset-1]

# Instantiate arrays for inputs and outputs
train_inputs = []
train_outputs = np.array([])

test_inputs = []
test_expected_outputs = np.array([])
test_actual_outputs = []

# Read training file
print 'Reading training file'
t = time()
for line in open('datasets/%s-train.txt' % filename):
  inputs = line.split(' ')
  output = inputs.pop()
  train_outputs = np.append(train_outputs, int(output))
  train_inputs.append(map(float, inputs))
print 'Done. Time taken: %f secs.\n' % (time()-t)

print 'Create classifier'
t = time()
clf = None

# No preprocessing for SVMs
# Otherwise, scale inputs (preprocessing to make more amenable for machine learning)
if classifier == 1: # Support vector machines
  clf = SVC()
elif classifier == 2: # Gaussian Naive Bayes
  train_inputs = preprocessing.scale(np.array(train_inputs))
  clf = GaussianNB()
elif classifier == 3: # Multinomial Naive Bayes
  clf = MultinomialNB()
elif classifier == 4: # Stochastic gradient descent with logistic regression
  train_inputs = preprocessing.scale(np.array(train_inputs))
  clf = SGDClassifier(loss='log')
print 'Done. Time taken: %f secs.\n' % (time()-t)

print 'Fit classifier'
t = time()
clf.fit(train_inputs, train_outputs)
print 'Done. Time taken: %f secs.\n' % (time()-t)

# Read test file and scale inputs
print 'Reading test file'
t = time()
for line in open('datasets/%s-test.txt' % filename):
  inputs = line.split(' ')
  output = inputs.pop()
  test_expected_outputs = np.append(test_expected_outputs, int(output))
  test_inputs.append(map(float, inputs))

# Same here: no preprocessing for SVMs
# Otherwise, scale inputs (preprocessing to make more amenable for machine learning)
if classifier != 1:
  test_inputs = preprocessing.scale(np.array(test_inputs))
print 'Done. Time taken: %f secs.\n' % (time()-t)

print 'Predict for test file'
t = time()
test_actual_outputs = [clf.predict(i)[0] for i in test_inputs]
print 'Done. Time taken: %f secs.\n' % (time()-t)

print 'Compare outputs'
t = time()
right = sum(test_actual_outputs == test_expected_outputs)
wrong = len(test_actual_outputs) - right
print 'Done. Time taken: %f secs.\n' % (time()-t)

print 'Number right: %d\nNumber wrong: %d' % (right, wrong)
print 'Prediction rate: %.2f%%' % (100.0 * right/len(test_actual_outputs))
print 'Total time taken: %f secs.\n' % (time()-t0)
