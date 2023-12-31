import numpy as np
import json
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

def data_processing(data):
	train_set, valid_set, test_set = data['train'], data['valid'], data['test']
	Xtrain = train_set[0]
	ytrain = train_set[1]
	Xval = valid_set[0]
	yval = valid_set[1]
	Xtest = test_set[0]
	ytest = test_set[1]

	Xtrain = np.array(Xtrain)
	Xval = np.array(Xval)
	Xtest = np.array(Xtest)

	ytrain = np.array(ytrain)
	yval = np.array(yval)
	ytest = np.array(ytest)
	
	return Xtrain, ytrain, Xval, yval, Xtest, ytest


def data_processing_with_transformation(data, do_minmax_scaling=True, do_normalization=False):
	train_set, valid_set, test_set = data['train'], data['valid'], data['test']
	Xtrain = train_set[0]
	ytrain = train_set[1]
	Xval = valid_set[0]
	yval = valid_set[1]
	Xtest = test_set[0]
	ytest = test_set[1]

	Xtrain = np.array(Xtrain)
	Xval = np.array(Xval)
	Xtest = np.array(Xtest)

	ytrain = np.array(ytrain)
	yval = np.array(yval)
	ytest = np.array(ytest)
	
	# We load data from json here and turn the data into numpy array
	# You can further perform data transformation on Xtrain, Xval, Xtest

	# Min-Max scaling
	if do_minmax_scaling:
		for i in range(Xtrain.shape[1]):
			train = Xtrain[:,i].copy()
			Xtrain[:,i] = (Xtrain[:,i] - train.min()) / (train.max() - train.min())
			Xval[:,i] = (Xval[:,i] - train.min()) / (train.max() - train.min())
			Xtest[:,i] = (Xtest[:,i] - train.min()) / (train.max() - train.min())
		
		#####################################################
		#				 YOUR CODE HERE					    #
		#####################################################
	
	# Normalization
	def normalization(x):
		#####################################################
		#				 YOUR CODE HERE					    #
		#####################################################
		# print(x)
		for i in range(x.shape[0]):
			x[i,:] = x[i,:] / np.linalg.norm(x[i,:])
		# x += 0.0000000000001
		# x_norm = np.linalg.norm(x, ord = 2)
		# x = np.divide(x, x_norm)
		# print(x)
		return x
	
	if do_normalization:
		Xtrain = normalization(Xtrain)
		Xval = normalization(Xval)
		Xtest = normalization(Xtest)

	return Xtrain, ytrain, Xval, yval, Xtest, ytest


def compute_l2_distances(Xtrain, X):
	"""
	Compute the distance between each test point in X and each training point
	in Xtrain.
	Inputs:
	- Xtrain: A numpy array of shape (num_train, D) containing training data
	- X: A numpy array of shape (num_test, D) containing test data.
	Returns:
	- dists: A numpy array of shape (num_test, num_train) where dists[i, j]
	  is the Euclidean distance between the ith test point and the jth training
	  point.
	"""
	#####################################################
	#				 YOUR CODE HERE					    #
	#####################################################
	dists = np.zeros(shape=(X.shape[0], Xtrain.shape[0]))
	for i in range(X.shape[0]):
		for j in range(Xtrain.shape[0]):
			
			# dists[i][j] = np.linalg.norm((Xtrain[j] - X[i]))
			sqsum = 0
			for a,b in zip(Xtrain[j], X[i]):
				sqsum += (a-b) ** 2
			dists[i][j] = float(np.sqrt(sqsum))
	return dists


def compute_cosine_distances(Xtrain, X):
	"""
	Compute the distance between each test point in X and each training point
	in Xtrain.
	Inputs:
	- Xtrain: A numpy array of shape (num_train, D) containing training data
	- X: A numpy array of shape (num_test, D) containing test data.
	Returns:
	- dists: A numpy array of shape (num_test, num_train) where dists[i, j]
	  is the Cosine distance between the ith test point and the jth training
	  point.
	"""
	#####################################################
	#				 YOUR CODE HERE					    #
	#####################################################
	dists = np.zeros(shape=(X.shape[0], Xtrain.shape[0]))
	for i in range(X.shape[0]):
		for j in range(Xtrain.shape[0]):
			normxt = np.linalg.norm(Xtrain[j]) + 0.00000000001
			normx = np.linalg.norm(X[i]) + + 0.00000000001

			dists[i][j] = 1 - (np.dot(Xtrain[j], X[i]) / (normxt * normx))
	return dists


def predict_labels(k, ytrain, dists):
	"""
	Given a matrix of distances between test points and training points,
	predict a label for each test point.
	Inputs:
	- k: The number of nearest neighbors used for prediction.
	- ytrain: A numpy array of shape (num_train,) where ytrain[i] is the label
	  of the ith training point.
	- dists: A numpy array of shape (num_test, num_train) where dists[i, j]
	  gives the distance betwen the ith test point and the jth training point.
	Returns:
	- ypred: A numpy array of shape (num_test,) containing predicted labels for the
	  test data, where y[i] is the predicted label for the test point X[i].
	"""
	#####################################################
	#				 YOUR CODE HERE					    #
	#####################################################
	ypred = np.zeros(shape=dists.shape[0])
	for i in range(dists.shape[0]):
		row = [[dists[i][j], ytrain[j]] for j in range(dists.shape[1])]
		row.sort()
		nearest_labels = [x[1] for x in row[1:k+1]]
		#print("=========")
		#print(row)
		#print(nearest_labels)
		counter = Counter(nearest_labels)
		likely_label, _ = counter.most_common(1)[0]
		#print(counter.most_common(1)[0])
		ypred[i] = likely_label
	
	return ypred


def compute_error_rate(y, ypred):
	"""
	Compute the error rate of prediction based on the true labels.
	Inputs:
	- y: A numpy array with of shape (num_test,) where y[i] is the true label
	  of the ith test point.
	- ypred: A numpy array with of shape (num_test,) where ypred[i] is the
	  prediction of the ith test point.
	Returns:
	- err: The error rate of prediction (scalar).
	"""
	#####################################################
	#				 YOUR CODE HERE					    #
	#####################################################
	wrong = len([ypred[i] for i in range(ypred.shape[0]) if ypred[i] != y[i]])
	err = wrong / y.shape[0]
	return err


def find_best_k(K, ytrain, dists, yval):
	"""
	Find best k according to validation error rate.
	Inputs:
	- K: A list of ks.
	- ytrain: A numpy array of shape (num_train,) where ytrain[i] is the label
	  of the ith training point.
	- dists: A numpy array of shape (num_test, num_train) where dists[i, j]
	  is the distance between the ith test point and the jth training
	  point.
	- yval: A numpy array with of shape (num_val,) where y[i] is the true label
	  of the ith validation point.
	Returns:
	- best_k: The k with the lowest error rate.
	- validation_error: A list of error rate of different ks in K.
	- best_err: The lowest error rate we get from all ks in K.
	"""
	#####################################################
	#				 YOUR CODE HERE					    #
	#####################################################
	validation_error = []
	best_k = 0
	# alle = []
	for k in range(len(K)):
		ypred = predict_labels(K[k], ytrain, dists)
		error = compute_error_rate(yval, ypred)
		validation_error.append(error)
		if validation_error[best_k] > error:
			best_k = k
	best_err = validation_error[best_k]
	print(validation_error)
	return K[best_k], validation_error, best_err


def main():
	input_file = 'disease.json'
	output_file = 'knn_output.txt'

	#==================Problem Set 1.1=======================

	with open(input_file) as json_data:
		data = json.load(json_data)

	# Compute distance matrix
	Xtrain, ytrain, Xval, yval, Xtest, ytest = data_processing(data)

	dists = compute_l2_distances(Xtrain, Xval)

	# Compute validation accuracy when k=4
	k = 4
	ypred = predict_labels(k, ytrain, dists)
	err = compute_error_rate(yval, ypred)
	print("The validation error rate is", err, "in Problem Set 1.1")
	print()
 
	#==================Problem Set 1.2=======================

	# Compute distance matrix
	Xtrain, ytrain, Xval, yval, Xtest, ytest = data_processing_with_transformation(data, do_minmax_scaling=False, do_normalization=True)

	dists = compute_l2_distances(Xtrain, Xval)

	# Compute validation accuracy when k=4
	k = 4
	ypred = predict_labels(k, ytrain, dists)
	err = compute_error_rate(yval, ypred)
	print("The validation error rate is", err, "in Problem Set 1.2 when using normalization")
	print()

	# Compute distance matrix
	Xtrain, ytrain, Xval, yval, Xtest, ytest = data_processing_with_transformation(data, do_minmax_scaling=True, do_normalization=False)

	dists = compute_l2_distances(Xtrain, Xval)

	# Compute validation accuracy when k=4
	k = 4
	ypred = predict_labels(k, ytrain, dists)
	err = compute_error_rate(yval, ypred)
	print("The validation error rate is", err, "in Problem Set 1.2 when using minmax_scaling")
	print()
	
	#==================Problem Set 1.3=======================

	# Compute distance matrix
	Xtrain, ytrain, Xval, yval, Xtest, ytest = data_processing(data)
	dists = compute_cosine_distances(Xtrain, Xval)

	# Compute validation accuracy when k=4
	k = 4
	ypred = predict_labels(k, ytrain, dists)
	err = compute_error_rate(yval, ypred)
	print("The validation error rate is", err, "in Problem Set 1.3, which use cosine distance")
	print()

	#==================Problem Set 1.4=======================
	# Compute distance matrix
	Xtrain, ytrain, Xval, yval, Xtest, ytest = data_processing(data)

	#======performance of different k in training set=====
	K = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18]
	#####################################################
	#				 YOUR CODE HERE					    #
	#####################################################
	dists = compute_l2_distances(Xtrain, Xtrain)
	best_k, validation_error, best_err = find_best_k(K, ytrain, dists, ytrain)

	plt.figure()
	plt.xticks(K)
	plt.plot(K, validation_error)
	plt.ylabel('Error rate')
	plt.xlabel('K')
	plt.title('Training error')
	plt.savefig('train.png')

	dists = compute_l2_distances(Xtrain, Xtest)
	best_k, validation_error, best_err = find_best_k(K, ytrain, dists, ytest)
	plt.figure()
	plt.xticks(K)
	plt.plot(K, validation_error)
	plt.ylabel('Error rate')
	plt.xlabel('K')
	plt.title('Testing error')
	plt.savefig('test.png')
	#==========select the best k by using validation set==============
	dists = compute_l2_distances(Xtrain, Xval)
	best_k, validation_error, best_err = find_best_k(K, ytrain, dists, yval)
	plt.figure()
	plt.xticks(K)
	plt.plot(K, validation_error)
	plt.ylabel('Error rate')
	plt.xlabel('K')
	plt.title('Validation error')
	plt.savefig('val.png')
	#===============test the performance with your best k=============
	dists = compute_l2_distances(Xtrain, Xtest)
	ypred = predict_labels(best_k, ytrain, dists)
	test_err = compute_error_rate(ytest, ypred)
	print("In Problem Set 1.4, we use the best k = ", best_k, "with the best validation error rate", best_err)
	print("Using the best k, the final test error rate is", test_err)
	#====================write your results to file===================
	f=open(output_file, 'w')
	for i in range(len(K)):
		f.write('%d %.3f' % (K[i], validation_error[i])+'\n')
	f.write('%s %.3f' % ('test', test_err))
	f.close()

	best = float("inf")
	bestk = -1
	alle = []
	for k in K:
		neigh = KNeighborsClassifier(n_neighbors=k, metric='l2')
		neigh.fit(Xtrain, ytrain)
		sypred = neigh.predict(Xtest)
		e = compute_error_rate(ytest, sypred)
		alle.append(e)
		if e < best:
			best = e
			bestk = k
	print('sklearn')
	print(best)
	print(bestk)
	print(alle)
if __name__ == "__main__":
	main()
