import numpy as np
import random

LEARNING_RATE = 0.01

class Neuron:
	def __init__(self, input_size):
		self.threshold = 0.5
		self.weights = np.zeros((input_size)).astype(float)
		for i in range(input_size):
			self.weights[i] = random.random()

	def step_func(self, weighted_avg):
		return int(weighted_avg > self.threshold)

	def fire(self, inputs): # inputs is a vector with the same length as self.weights
		return self.step_func(inputs.dot(self.weights) / np.sum(self.weights))

class Layer:
	def __init__(self, layer_number, number_of_neurons, number_of_inputs):
		self.neurons = []
		for i in range(number_of_neurons):
			temp = Neuron(number_of_inputs)
			self.neurons.append(temp)
		self.id = layer_number

	def fire(self, inputs):
		return np.array([n.fire(inputs) for n in self.neurons])

class Network:
	def __init__(self, layer_sizes):
		self.layers = []
		for i in range(len(layer_sizes) - 1):
			self.layers.append(Layer(i + 1, layer_sizes[i + 1], layer_sizes[i]))

	def fire(self, inputs):
		state = inputs
		layer_states = []
		for layer in self.layers:
			layer_states.append(state)
			state = layer.fire(state)
		return state[0], layer_states

	def train(self, inputs, outputs, iterations):
		for i in range(iterations):
			for j in range(len(inputs)):
				actual, layer_states = self.fire(inputs[j])
				expected = outputs[j]
				diff = expected - actual
				for k in range(len(layer_states)):
					current_layer = self.layers[k]
					current_state = layer_states[k]
					for neuron in current_layer.neurons:
						for l in range(len(current_state)):
							if current_state[l]:
								neuron.weights[l] += LEARNING_RATE * diff
					if k > 0:
						for l in range(len(current_state)):
							if current_state[l]:
								self.layers[k - 1].neurons[l].threshold -= LEARNING_RATE * diff

	def classify(self, input):
		return self.fire(input)[0]

	def to_string(self):
		for i in range(len(self.layers)):
			for j in range(len(self.layers[i].neurons)):
				neuron = self.layers[i].neurons[j]
				print(i)
				print(j)
				print(neuron.weights)
				print(neuron.threshold)
				print()

inputs = [np.array([0, 0, 1]), np.array([0, 1, 1]), np.array([1, 0, 1]), np.array([1, 1, 1])]
outputs = [0, 1, 1, 0]
a = Network([3,2,1])
a.train(inputs, outputs, 50000)
print(a.classify(np.array([0, 0, 1])))
print(a.classify(np.array([0, 1, 1])))
print(a.classify(np.array([1, 0, 1])))
print(a.classify(np.array([1, 1, 1])))
#print(a.fire(np.array([0.3,0.6,0.7])))
