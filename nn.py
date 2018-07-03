#Neural network and functions for it

import numpy as np
import aux

#Classes for activation function are elementwise. They return vectors (matrices) of the same size: value and derivative for each element
def Softsign(matrix):
	return matrix/(1+abs(matrix)),pow((1+abs(matrix)),-2)

#Classes for cost function take vector (matrix) of calculated values, vector (matrix) of given values, and return scalar penalty and derivatives for calculated value (same size)
def SquaredCostfunc(calculated,output):
	y=calculated-output
	return sum(sum(pow(y,2))),2*y

#Classes for penalty take vector of coefficients and return penalty (scalar) and derivatives for it 
def MixedPenalty(parameters,squared=0.1,absval=0.1):
	return squared*sum(pow(parameters,2))+absval*sum(abs(parameters)),2*squared*parameters+absval*np.sign(parameters)

#class representing neural network, which can execute and learn
class Network:
	#Defining parameters for calculation and learning.
	#Neuron number is a list of integers. It's length is number of layers plus one.
	#It's first parameter is the number of inputs, the following parameters are number of neurons in the layer.
	#For example, [4,10,1] is a network with two layers, four inputs, 10 neurons on the first layer, 1 neuron on the second layer (and one output).
	def __init__(self,neuron_number,activator=Softsign,costfunc=SquaredCostfunc,penalty=MixedPenalty):
		self.activator=activator
		self.costfunc=costfunc
		self.penalty=penalty
		self.layers=len(neuron_number)-1
		self.matr_wid=[neuron_number[j]+1 for j in xrange(self.layers)]
		self.matr_hei=[neuron_number[j+1] for j in xrange(self.layers)]
		self.matr_sz=[self.matr_wid[j]*self.matr_hei[j] for j in xrange(self.layers)]
	#Function for both learning and calculation. In calculation mode (if output is set to None), gets input and parameters (of the NN) and returns results.
	#In learning mode, it accepts output and returns value to optimize (scalar) and gradient.
	def calculate(self,input,parameters,output=None,verbose=False):
		matrices=self.__decode__(parameters)
		vectors=[None]*(self.layers+1)
		vectors[0]=input
		derivatives=[None]*(self.layers+1)
		derivative_matrices=[None]*self.layers
		hist_dy,hist_dba=[None]*(self.layers+1),[None]*(self.layers+1)
		for j in xrange(self.layers):
			vectors[j]=np.concatenate([vectors[j],np.ones([1,vectors[j].shape[1]])],axis=0) #here we append ones to the bottom to imitate b 
			(vectors[j+1],derivatives[j])=self.activator(np.matmul(matrices[j],vectors[j]))
		if(output is None):
			return vectors[self.layers]
		y,dy=self.costfunc(vectors[self.layers],output)
		derivatives[self.layers]=dy
		for j in xrange(self.layers,0,-1):
			derivatives_before_activation=dy*derivatives[j-1];
			derivative_matrices[j-1]=np.matmul(derivatives_before_activation,vectors[j-1].T)
			dy=np.matmul(matrices[j-1].T,derivatives_before_activation)
			dy=dy[:-1,:]
			hist_dy[j-1],hist_dba[j-1]=dy,derivatives_before_activation
		gradient=self.__encode__(derivative_matrices)
		p,dp=self.penalty(parameters)
		if verbose:
			aux.__OutputNN__(self.layers,matrices,derivative_matrices,vectors,hist_dy,hist_dba)
		return p+y,dp+gradient
	#size of initial vector
	def initialParametersSize(self):
		return sum(self.matr_sz)
	#vector to array of matrices
	def __decode__(self,parameters):
		def to_matr(vector,width,height):
			return np.concatenate([np.take(vector,xrange(j*width,(j+1)*width),axis=0).T for j in xrange(height)],axis=0)
		matrices=[]
		idx=0
		for j in xrange(self.layers):
			matrices.append(to_matr(np.take(parameters,xrange(idx,idx+self.matr_sz[j]),axis=0),self.matr_wid[j],self.matr_hei[j]))
			idx=idx+self.matr_sz[j]
		return matrices
	#array of matrices to vector
	def __encode__(self,matrices):
		def to_vect(matrix):
			return np.concatenate([np.take(matrix,[j],axis=0) for j in xrange(matrix.shape[0])],axis=1)
		return np.concatenate([to_vect(matrices[j]) for j in xrange(self.layers)],axis=1).T
