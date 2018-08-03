#
# Tests 

import numpy as np
import nn
import opt
import aux
import allpass_rules
import players
import random
reload(nn)
reload(opt)
reload(aux)
reload(allpass_rules)
reload(players)
reload(nn)
reload(opt)
reload(aux)

def test_Derivatives():
	a1=np.array([[0.0]])
	a2=np.array([[1],[-1],[0.1]])
	assert(aux.testDerivative(nn.Softsign,a1))
	assert(aux.testDerivative(nn.MixedPenalty,a2))
	assert(aux.testDerivative(lambda x:nn.MixedPenalty(x,squared=0.2,absval=0.3),a2))
	assert(aux.testDerivative(lambda x:nn.SquaredCostfunc(x,np.array([[1],[2],[3]])),a2))
	print "Tests passed."

def test_EncDecode():	
	net=nn.Network([3,2,3])
	ip=np.array([xrange(net.initialParametersSize())]).T
	mc=net.__decode__(ip);
	fv=net.__encode__(mc);
	print ip
	print mc
	print fv
	assert(all(fv==ip))
	print "Tests passed."

def test_Network():
	shape=[2,2,2]
	net=nn.Network(shape)
	coef=np.array([xrange(net.initialParametersSize())]).T*0.1+1e-12
	input=np.array([[0.4,0.5],[6.0,7]]);
	out=np.array([[0.1,0.8],[2,1.1]]);
	net.calculate(input,coef,out,verbose=True)
	assert(aux.testDerivative(lambda x:net.calculate(input,x,out),coef))
	print "Tests passed."

def test_Rosenbrock():
	assert(aux.testDerivative(aux.rosenbrock,np.array([[0.5,0.5]]).T,verbose=False))
	assert(aux.testDerivative(aux.rosenbrock,np.array([[0.8,0.6]]).T,verbose=False))
	assert(aux.testDerivative(lambda x:aux.rosenbrock(x,10),np.array([xrange(0,5)]).T*0.1,verbose=False))
	print "Tests passed."

def test_Linearf():
	assert(aux.testDerivative(aux.linear,np.array([[73,10.0]]).T,verbose=False))
	print "Test passed."
	
def test_OptAlgoArbitary(algorithm,f,dim=2,threshdy=1e-8):
	hist=aux.Historian(f)
	start=np.zeros((dim,1))
	x,dummy=algorithm(lambda x:hist.f(x),start,threshdy)
	y,dy=f(x)
	print 'Answer',x.T
	print 'Value',y
	print 'Deivatives',dy.T
	print 'Steps',hist.num
	assert(max(max(abs(dy)))<threshdy)
	print "Tests passed."
	return hist

def test_OptAlgo(algorithm,coef=100.0,dim=2,threshdy=1e-8):
	f=lambda x:aux.rosenbrock(x,coef)
	test_OptAlgoArbitary(algorithm,f,dim,threshdy)
	
#Note that basic algorithm currently optimizes Rosenbrock function in 31455 iterations.
def test_optBasic():
	test_OptAlgo(opt.optimizeSimple)

def test_optLinearNewton():
	algorithm=lambda f,x,threshdy:opt.optimizeAdvanced(f,x,threshdy,rset_steps=1,newton_steps=1)
	test_OptAlgoArbitary(algorithm,aux.linear)

def test_optLinearFull():
	algorithm=lambda f,x,threshdy:opt.optimizeAdvanced(f,x,threshdy,rset_steps=3,newton_steps=1)
	test_OptAlgoArbitary(algorithm,aux.linear)

def test_optRsBaseVersion():
	algorithm=lambda f,x,threshdy:opt.optimizeAdvanced(f,x,threshdy,rset_steps=0,newton_steps=0)
	test_OptAlgo(algorithm)

def test_optRsNewton():
	algorithm=lambda f,x,threshdy:opt.optimizeAdvanced(f,x,threshdy,rset_steps=1,newton_steps=3)
	test_OptAlgo(algorithm)
	
def test_optRsOrt():
	algorithm=lambda f,x,threshdy:opt.optimizeAdvanced(f,x,threshdy,rset_steps=2,newton_steps=0)
	test_OptAlgo(algorithm)
	
def test_optRsNewtonOrt():
	algorithm=lambda f,x,threshdy:opt.optimizeAdvanced(f,x,threshdy,rset_steps=2,newton_steps=3)
	test_OptAlgo(algorithm)

#Note that advanced algorithm currently optimizes Rosenbrock function in 170 iterations.
def test_optRsDefault():
	algorithm=lambda f,x,threshdy:opt.optimizeAdvanced(f,x,threshdy)
	test_OptAlgo(algorithm)
	
def test_WholeOpt():
	test_optLinearNewton()
	test_optLinearFull()
	test_optRsBaseVersion()
	test_optRsNewton()
	test_optRsOrt()
	test_optRsNewtonOrt()
	test_optRsDefault()

def test_gamePlay(cards):
	pl=[players.FastRandomPlayer() for j in xrange(3)]
	allpass_rules.play(pl,cards,True)

