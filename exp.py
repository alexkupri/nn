#
#Main file with experiments

import numpy as np
import nn
import opt
import aux
reload(nn)
reload(opt)
reload(aux)

#for each column vector calculate, if it belongs to sphere or radius 1
def sphere(x):
	return np.array([-np.sign(sum(pow(x,2))-1)])

def output_statistics(ground_truth,network_output,comment):
	n=ground_truth.shape[1]
	spheres=sum(1 if ground_truth[0,j]>0 else 0 for j in xrange(n))
	errors=sum(1 if ground_truth[0,j]*network_output[0,j]<0 else 0 for j in xrange(n))
	fpositives=sum(1 if ground_truth[0,j]<0 and network_output[0,j]>0 else 0 for j in xrange(n))
	fnegatives=sum(1 if ground_truth[0,j]>0 and network_output[0,j]<0 else 0 for j in xrange(n))
	p=n*0.01
	print comment
	print "Samples=",n,"spheres=",spheres,"(",spheres/p,"%)","errors=",errors,"(",errors/p,"%)"
	print "False negatives=",fnegatives,"(",fnegatives/p,"%)","fpositives=",fpositives,"(",fpositives/p,"%)"
	print "False negatives rate=",fnegatives*100.0/spheres,"% False positives rate=",fpositives*100.0/(n-spheres),"%"
	print ""
	
#Note that outputs of NN are currently in (-1,1)
def sphere_experiment(dim,samples,network_shape,penalty=nn.MixedPenalty,proving_samples=1000):
	print "Starting experiment on spheres of dimension",dim,"learning samples=",samples,"shape",network_shape
	input=np.random.rand(dim,samples)*4-2 #All values belong to [-2,2]
	#input=aux.regularGrid()
	output=sphere(input)
	assert(len(network_shape)>=2 and network_shape[0]==dim and network_shape[-1]==1)
	network=nn.Network(network_shape,penalty=penalty)
	parameters,err=opt.optimizeNetwork(network,input,output)
	proving_input=np.random.rand(dim,proving_samples)*4-2
	proving_output=sphere(proving_input)
	network_on_learning=network.calculate(input,parameters)
	network_on_new=network.calculate(proving_input,parameters)
	output_statistics(output,network_on_learning,"Learning subset")
	output_statistics(proving_output,network_on_new,"New subset")

def exp_sphere1():
	sphere_experiment(2,100,[2,3,1])
