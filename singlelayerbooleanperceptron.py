import numpy as np

# a OR b, third input is bias

OR_training = [
	[np.array([0.0, 0.0, 1.0]), 0],
	[np.array([0.0, 1.0, 1.0]), 1],
	[np.array([1.0, 0.0, 1.0]), 1],
	[np.array([1.0, 1.0, 1.0]), 1]
]
AND_training = [
	[np.array([0.0, 0.0, 1.0]), 0],
	[np.array([0.0, 1.0, 1.0]), 0],
	[np.array([1.0, 0.0, 1.0]), 0],
	[np.array([1.0, 1.0, 1.0]), 1]
]
test = [i[0] for i in OR_training]
learning_rate = 0.01
iterations = 500

def train(training_data, learning_rate, iterations):
	weights = np.ones((training_data[0][0].shape))
	threshold = 0.5
	step_func = lambda x, t: int(x > t)

	for i in range(iterations):
		for d in training_data: # source: http://computing.dcu.ie/~humphrys/Notes/Neural/single.neural.html
			actual = step_func(weights.dot(d[0]), threshold)
			expected = d[1]
			threshold -= learning_rate * (expected - actual)
			weights = weights * (1 + (learning_rate * (expected - actual)))

	return weights, threshold

def classify(weights, threshold, data):
	outputs = []
	step_func = lambda x, t: int(x > t)
	
	for d in data:
		outputs.append(step_func(weights.dot(d), threshold))

	return outputs

weights, threshold = train(OR_training, learning_rate, iterations)
print(weights)
print(threshold)
print(classify(weights, threshold, test))
