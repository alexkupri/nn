#
#Optimization algorithms

import numpy as np
import nn
import aux

def optimizeSimple(f,x,threshdy=1e-8):
	step=-1.0
	y,dy=f(x)
	while max(max(abs(dy)))>threshdy:
		step1,step2=step*1.5,step*0.5
		y1,dy1=f(x+dy*step1)
		y2,dy2=f(x+dy*step2)
		if y1>y and y2>y:
			step=step*0.25 #even the best result is worse than current point, decrease step
		elif y1<y2:
			x,y,dy,step=x+dy*step1,y1,dy1,step1
		else:
			x,y,dy,step=x+dy*step2,y2,dy2,step2
	return x,y

def dot(x,y):
	return np.matmul(x.T,y)[0][0]

def optimizeAdvanced(f,x,threshdy=1e-8,rset_steps=5,newton_steps=3,thresh_step=1e-18):
	y,dy=f(x)
	search=-dy
	until_rset=rset_steps
	an=1
	while max(max(abs(dy)))>threshdy:#main iteration, changing directions
		oldx=x
		a1,a2=0.0,an
		y2,dy2=f(x+a2*search)
		while dot(dy2,search)<0:#searching the point where the derivative changes (unlikely)
			a2=a2*2.0
			y2,dy2=f(x+a2*search)
		an,yn,dyn=a2,y2,dy2
		y1,dy1=y,dy
		skipn=False;
		for j in xrange(newton_steps): #a few Newton iterations along the search direction, so that new 
			da=a2-a1;
			if skipn:
				an=0.5*(a1+a2)				
			else:
				an=a1-(a2-a1)/(dot(dy2,search)-dot(dy1,search))*dot(dy1,search)
			yn,dyn=f(x+an*search)
			if dot(dyn,search)<0: #negative at the left, positive at the right
				a1,y1,dy1=an,yn,dyn
			else:
				a2,y2,dy2=an,yn,dyn
			skipn=(a2-a1)*1.5>da
		while (dot(dyn,search)>dot(search,search) or not np.isfinite(yn))and an>0: #if the function is "strange" or Newton did not converge properly 
			#(e.g. very multimodal or first derivatives are zero), we make step smaller and smaller until we found a next smaller value
			an=an*0.5
			yn,dyn=f(x+an*search)
			until_rset=0
		until_rset=until_rset-1
		new_search=-dyn+dot(dyn,dyn)/dot(dy,dy)*search
		if until_rset<=0 or dot(new_search,dyn)>0: #each n iterations we reset the value
			until_rset=rset_steps
			new_search=-dyn
		x,y,dy,search=x+an*search,yn,dyn,new_search
		if max(max(abs(oldx-x)))<thresh_step:
			break #This most probably means we have infinite value.
	return x,y

#putting all together, and some sort of avoiding saddles (see below)
def optimizeNetwork(network,input,output):
	start=np.random.randn(network.initialParametersSize(),1)*0.01
	#start=np.array([[-0.00526866, -0.0050952,   0.00709853, -0.0038618,  -0.01170891, -0.00592323,
#					0.00449048,  0.00071054,  0.00239297,  0.00394111, -0.01361386,  0.01486778,  -0.01597716]]).T
	print start.T
	hist=aux.Historian(lambda x:network.calculate(input,x,output))
	func=lambda x:hist.f(x)
	nx,ny=optimizeAdvanced(func,start)
	#return nx,ny
	while True: #Sort of global optimization to exit saddles
		ox,oy=nx,ny
		nx,ny=optimizeAdvanced(func,ox+np.random.randn(network.initialParametersSize(),1)*0.01)
		if ny>=oy:
			print "The algorithm converged in",hist.num,"steps"
			return ox,oy
