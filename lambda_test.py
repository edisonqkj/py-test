def btn(x,y,func):
	return func(x,y)

if __name__=='__main__':
	import math
	print (btn(2,3, lambda x,y: math.pow(x,y)))