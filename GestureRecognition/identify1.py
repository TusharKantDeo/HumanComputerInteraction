import random
# Third-party libraries
import numpy as np


def feedforward(a):
	from cast_spell import s
	from cast_spell import t
        """Return the output of the network if ``a`` is input."""
	for b, w in zip(s,t):
		a=np.asarray(a)
		print ""
		a = sigmoid(np.dot(w, a)+b)
	return a

def evaluate(test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
	#print test_data
	test_results = [(np.argmax(feedforward(x)))
                    for x in test_data]
	return test_results[0]
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))