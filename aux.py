#
#Staff for testing and output

import numpy as np

#class intended to save history of calculation and safely call the function
class Historian:
	def __init__(self,func,tracex=False,tracey=False,tracedy=False,makeout=False):
		self.func,self.x,self.y,self.dy,self.num,self.good,self.makeout=func,None,None,None,0,True,makeout
		if tracex:
			x=[]
		if tracey:
			y=[]
		if tracedy:
			dy=[]
	def f(self,x):
		try:
			y,dy=self.func(x)
		except KeyboardInterrupt:
			raise
		except:
			y,dy=np.Inf,np.zeros(x.shape)
		if not (np.isfinite(y) and np.isfinite(dy).all):
			y,dy=np.Inf,np.zeros(x.shape)
		if self.good and not np.isfinite(y):
			print "An error occured. Make sure that all functions are compatible. x="
			print x.T
			self.good=False			
		if not self.x is None:
			self.x.append(x);
		if not self.y is None:
			self.y.append(y);
		if not self.dy is None:
			self.dy.append(dy);
		self.num=self.num+1;
		if self.makeout:
			print x.T,y,dy.T
		return y,dy

#Calculates the gradient numerically
def numericalGradient(f,point,alpha):
	(y,dummy)=f(point)
	res=np.zeros(point.shape)
	for j in xrange(res.shape[0]):
		mypoint=point.copy()
		mypoint[j,0]=mypoint[j,0]+alpha
		(dy,dummy)=f(mypoint)
		res[j,0]=(dy-y)/alpha
	return res

#Proves, if the derivative is calculated correctly
def testDerivative(f,point,rtol=0.01,atol=0.01,verbose=True,startp=1.0,endp=1e-12):
	a=startp
	passed=False
	(y,aGradient)=f(point)
	bestat=np.Inf
	while a>endp:
		numGradient=numericalGradient(f,point,a)
		rt=max(abs(numGradient-aGradient))
		at=max(2*abs(numGradient-aGradient)/(abs(numGradient)+abs(aGradient)+1e-308))
		if at<atol or rt<rtol:
			passed=True
		if at<bestat:
			bestat,besta,bestNumGradient=at,a,numGradient
		a=a/2
	if verbose or not passed:
		print "x ",point.T
		print "f ",y
		print "best coincidence was at ",besta, "atol", bestat
		print "numGradient", bestNumGradient.T
		print "aGradient  ", aGradient.T
		print "Final gradient", numGradient.T
		print "Derivative test passed" if passed else "Failed"
	return passed

#Rosenbrock function, very hard function to optimize
def rosenbrock(x,coef=100):
	dy=np.zeros(x.shape);
	y=0
	for j in xrange(x.shape[0]-1):
		y=y+coef*pow((x[j+1,0]-pow(x[j,0],2)),2)+pow(1.0-x[j,0],2)
		dy[j,0]=dy[j,0]+4*coef*(pow(x[j,0],3)-x[j,0]*x[j+1,0])+2*x[j,0]-2
		dy[j+1,0]=dy[j+1,0]+2*coef*(x[j+1,0]-pow(x[j,0],2))
	return y,dy

#Linear equation as optimization problem, solution is 2,-2
def linear(x):
	A,b=np.array([[3.0,2],[2,8]]),np.array([[25,88.0]]).T
	return 0.5*np.matmul(x.T,np.matmul(A,x))[0,0]-np.matmul(b.T,x)[0,0],np.matmul(A,x)-b

#Output intermediate values of the NN
def __OutputNN__(layers,matrices,derivative_matrices,vectors,dy,derivatives_before_activation):
	for j in xrange(layers):
		print "layer", j
		print "vector"
		print vectors[j]
		print "derivatives"
		print dy[j]
		print "matrix"
		print matrices[j]
		print "derivative_matrices"
		print derivative_matrices[j]
		print "multipled"
		print np.matmul(matrices[j],vectors[j])
		print "derivs before activation"
		print derivatives_before_activation[j]
	print "finally"
	print "vector"
	print vectors[layers]
	print "derivatives"
	print dy[layers]

#Debug staff
def regularGrid():
	return np.array([[j/10 for j in xrange(100)] ,[j%10 for j in xrange(100)]])*0.2-0.9
