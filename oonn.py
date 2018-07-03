import numpy as np

#variables I as number of inputs, O as number of outputs, P as number of params
#prop(x,params) -> y, immediate_penalty
#bprop(dy/dx[j+1]) -> dy/dx[j], dy/dparams
#clone - as the objects are not stateless and Symmetrical has many blocks, we must be able to clone them.

#class for multiplication by coefficients
class Multiplier:
	def __init__(self,m,n):
		self.I,self.O,self.P=m,n,(m+1)*n
	def prop(self,x,params):
		self.matrix=np.concatenate([np.take(vector,xrange(j*width,(j+1)*width),axis=0).T for j in xrange(height)],axis=0)
		self.vector=np.matmul(self.matrix,np.concatenate([vectors[j],np.ones([1,vectors[j].shape[1]])],axis=0))
		return self.vector,0.0
	def bprop(self,dy):
		dprevy=np.matmul(self.matrix.T,dy)
		dmatrix=np.matmul(dy,self.vector)
		return dy[:-1,:],np.concatenate([np.take(dmatrix,[j],axis=0) for j in xrange(dmatrix.shape[0])],axis=1)
	def clone(self):
		return Multiplier(self.m,self.n)

#class for applying activation function	
class Activator:
	def __init__(self,fun,width):
		self.fun,self.I,self.O,self.P=fun,width,width,0
	def prop(self,x,params):
		self.dy=self.fun(x)
		return self.y,0.0
	def bprop(self,dy):
		return dy*self.dy,np.ndarray((0,0))
	def clone(self):
		return self

#class for combining other elements sequentially (container)
class Sequential:
	def __init__(self,blocks):
		self.blocks,self.I,self.O,self.P=blocks,blocks[0].I,blocks[-1].O,sum(b.P for b in blocks)
		for j in xrange(len(blocks)-1):
			assert blocks[j].O == blocks[j+1].I
	def prop(self,x,params):
		sp,pen=0,0.0
		for b in self.blocks:
			x,cpen=b.prop(x,np.take(params,xrange(sp,sp+b.P),axis=1))
			sp,pen=sp+b.P,pen+cpen
		return x,pen
	def bprop(self,dy):
		dparams=[]
		for b in reversed(blocks):
			dy,cdparams=b.bprop(dy)
			dparams.append(cdparams)
		return dy,np.concatenate(reversed(dparams))
	def clone(self):
		return Sequential([b.clone() for b in self.blocks])

#class for combining other elements in parallel (container)
class Parallel:
	def __init__(self,blocks):
		self.blocks,self.I,self.O,self.P=blocks,sum(b.I for b in blocks),sum(b.O for b in blocks),sum(b.P for b in blocks)
	def prop(self,x,params):
		si,sp,y,pen=0,0,[],0.0
		for b in self.blocks:
			cy,cpen=x.prop(np.take(x,xrange(si,si+b.I),axis=1),np.take(params,xrange(sp,sp+b.P),axis=1))
			y.append(cy)
			si,sp,pen=si+b.I,sp+b.P,pen+cpen
		return np.concatenate(y,axis=1),pen
	def bprop(self,dy):
		dyprev,dparam,so=[],[],0
		for b in self.blocks:
			dyc,dpc=b.bprop(np.take(dy,xrange(so,so+b.O),axis=1))
			dyprev.append(dyc)
			dparam.append(dpc)
			so=so+b.O
		return np.concatenate(dyprev,axis=1),np.concatenate(dparam,axis=1)
	def clone(self):
		return Parallel([b.clone() for b in blocks])

#class for multiplying by a constant matrix (useful for unity matrix as no-operation, splitting and combinig (adding) signals)	
class ConstMatrix:
	#Unfortunately we don't have sparse matrices in numpy, only in scipy
	def __init__(self,matrix):
		self.matrix,self.I,self.O,self.P=matrix,matrix.shape[0],matrix.shape[1],0
	def prop(self,x,params):
		return np.matmul(self.matrix,x),0
	def bprop(self,dy):
		return np.matmul(self.matrix.T,dy),np.ndarray((0,0))
	def clone(self):
		return self

#class for symmetrical execution of the similar blocks	
class Symmetrical:
	def __init__(self,block,n):
		self.blocks,self.n,self.I,self.O,self.P=[block.clone() for j in xrange(n)],n,block.I*n,block.O*n,block.P
	def prop(self,x,params):
		y,pen=[],0.0
		for j in xrange(self.n):
			cury,curpen=self.blocks[j].prop(np.take(x,xrange(j*self.block.I,(j+1)*self.block.I),axis=1),params)
			y.append(cury)
			pen=pen+curpen
		return np.concatenate(y,axis=1),pen
	def bprop(self,dy):
		dy,dp=[],[]
		for j in xrange(self.n):
			curdy,curdp=self.blocks[j].bprop(np.take(dx,xrange(j*self.block.O,(j+1)*self.block.O),axis=1),params)
			dy.append(curdy)
			dp.append(curdp)
		return np.concatenate(dy),sum(dp)
	def clone(self):
		return Symmetrical(self.blocks[0],self.n)

#class for regularisation of coefficients	
class RegularizationTerm:
	def __init__(self,block,fun):
		self.block,self.fun,self.I,self.O,self.P=block,fun,block.I,block.O,block.P
	def prop(self,x,params):
		cpen,self.dpen=self.fun(params)
		n=x.shape[0]
		cpen,self.dpen=cpen*n,self.dpen*n
		y,pen=self.block(x,params)		
		return y,pen+sum(cpen)
	def bprop(self,dy):
		dy,dp=self.block.bprop(dy)
		return dy,dp+self.dpen
	def clone(self):
		return RegularizationTerm(self.block.clone(),fun)

#simple function for supervized learning	
def supervised_learn(inp,outp,params,net,errorFun):
	y,curpen=net.prop(inp,params)
	pen,curdy=errorFun(y,outp)
	dy,dp=net.bprop(curdy)
	return pen+curpen,dp
