# -*- coding: utf-8 -*-
"""CSCI 567 HW1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LeTXWoz4pY10TssmM3Rb3pZPQSgVGWEU
"""

import numpy as np
import matplotlib.pyplot as plt

"""Answer 5.1"""

d = 100 # dimensions of data
n = 1000 # number of data points
X = np.random.normal(0,1, size=(n,d))
w_true = np.random.normal(0,1, size=(d,1))
y = X.dot(w_true) + np.random.normal(0,0.5,size=(n,1))

wLS = np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), y)
y_pred = X.dot(wLS)
errorLS = ((y_pred - y)**2).sum()
print('ErrorLS=',errorLS)

w0 = np.zeros(shape = (d,1))
y_pred0 = X.dot(w0)
error0 = ((y_pred0 - y)**2).sum()
print('Error for w0=', error0)

dt = 100 # dimensions of data
nt = 1000 # number of data points
X_test = np.random.normal(0,1, size=(nt,dt))
y_test = X_test.dot(w_true) + np.random.normal(0,0.5,size=(nt,1))

y_pred_test = X_test.dot(wLS)
errorLS_test = ((y_pred_test - y_test)**2).sum()
print('Test errorLS=', errorLS_test)

"""Answer 5.2"""

N = 20
eta = 0.00005
weights1 = [np.zeros((d,1))]
errors1 = np.array([])
for j in range(N):
  last_w = weights1[-1]
  f = X.dot(last_w) - y
  grad = 2 * X.T.dot(f)
  new_w = last_w - eta * grad
  weights1.append(new_w)
  f = X.dot(last_w)
  err = ((y - f)**2).sum()
  errors1 = np.append(errors1, err)

eta = 0.0005
weights2 = [np.zeros((d,1))]
errors2 = np.array([])
for j in range(N):
  last_w = weights2[-1]
  f = X.dot(last_w) - y
  grad = 2 * X.T.dot(f)
  new_w = last_w - eta * grad
  weights2.append(new_w)
  f = X.dot(last_w)
  err = ((y - f)**2).sum()
  errors2 = np.append(errors2, err)

eta = 0.0007
weights3 = [np.zeros((d,1))]
errors3 = np.array([])
for j in range(N):
  last_w = weights3[-1]
  f = X.dot(last_w) - y
  grad = 2 * X.T.dot(f)
  new_w = last_w - eta * grad
  weights3.append(new_w)
  f = X.dot(last_w)
  err = ((y - f)**2).sum()
  errors3 = np.append(errors3, err)

plt.figure()
plt.xticks(np.arange(0,20, step=1))
plt.plot(errors1, label="lr = 0.00005")
plt.plot(errors2, label="lr = 0.0005")
plt.plot(errors3, label="lr = 0.0007")
plt.ylabel('loss')
plt.xlabel('epochs')
plt.title('Gradient Descent')
ax = plt.gca()
ax.set_ylim([100, 100000])
plt.legend()
plt.savefig('gradient_descent.png')
print(errors1[-1])
print(errors2[-1])
print(errors3[-1])

"""Answer 5.3"""

N = 1000
eta = 0.0005
sweights1 = [np.zeros((d,1))]
serrors1 = np.array([])
for j in range(N):
  last_w = sweights1[-1]
  Xs = X[j]
  ys = y[j]
  f = Xs.dot(last_w) - ys
  grad = grad = 2 * Xs.T*f
  new_w = last_w - eta * grad
  sweights1.append(new_w)
  f = Xs.dot(last_w)
  err = ((y - f)**2).sum()
  serrors1 = np.append(serrors1, err)

N = 1000
eta = 0.005
sweights2 = [np.zeros((d,1))]
serrors2 = np.array([])
for j in range(N):
  last_w = sweights1[-1]
  Xs = X[j]
  ys = y[j]
  f = Xs.dot(last_w) - ys
  grad = grad = 2 * Xs.T*f
  new_w = last_w - eta * grad
  sweights2.append(new_w)
  f = Xs.dot(last_w)
  err = ((y - f)**2).sum()
  serrors2 = np.append(serrors2, err)

N = 1000
eta = 0.01
sweights3 = [np.zeros((d,1))]
serrors3 = np.array([])
for j in range(N):
  last_w = sweights1[-1]
  Xs = X[j]
  ys = y[j]
  f = Xs.dot(last_w) - ys
  grad = grad = 2 * Xs.T*f
  new_w = last_w - eta * grad
  sweights3.append(new_w)
  f = Xs.dot(last_w)
  err = ((y - f)**2).sum()
  serrors3 = np.append(serrors3, err)

plt.figure()
plt.xticks(np.arange(0,1000, step=100))
plt.plot(serrors1, label="lr = 0.0005")
plt.plot(serrors2, label="lr = 0.005")
plt.plot(serrors3, label="lr = 0.01")
plt.ylabel('loss')
plt.xlabel('epochs')
plt.title('Stochastic Gradient Descent')
ax = plt.gca()
ax.set_ylim([100, 30000000])
plt.legend()
plt.savefig('stochastic_gd.png')
print(serrors1[-1])
print(serrors2[-1])
print(serrors3[-1])

