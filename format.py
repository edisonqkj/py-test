# -*- coding: utf-8 -*-
'''
	Format string into specific structure
	Chinese character is supported
'''
import os

def formatit(str):
	# A,B,C,D  -->  D\nA(B) -> C(D)
	n=str.strip('\n')
	n=n.strip(',')
	sub=n.split(',')
	head=sub[-2]+'('+sub[-1]+')\n'
	res=[]
	for i in range(1,len(sub)+1):
		if i % 2==1:
			res.append(sub[i-1]+'('+sub[i]+')')
	result=' -> '.join(res)+'\n'
	return head+result

def groupit(strs):
	# A\nB\nC\nD --> A\nB\n+\n\n+C\nD\n+\n\n
	# add a new line in every 5 rows
	# res=[i+'\n' if i%2==0 for i in strs]
	# result=[i+'\n\n\n' if i%10==0 for i in res]
	# [i if i>2 else i-1 for i in a]
	result=[]
	for index,item in enumerate(strs):
		if (index+1)%2==0:
			result.append(item+'\n')
		elif (index+1)%10==0:
			result.append(item+'\n\n\n')
		else:
			result.append(item)

	# n=str.strip('\n')
	# n=n.strip(',')
	# sub=n.split(',')
	# res=[]
	# for i in range(1,len(sub)+1):
	# 	if i % 2==1:
	# 		res.append(sub[i-1]+'('+sub[i]+')')
	# result=' -> '.join(res)+'\n'
	return result

if __name__ == '__main__':
	f=u'tool.csv'
	csv=open(f,'r')
	csv.readline()
	content=csv.readlines()
	csv.close()
	# print(','.join(content).encode('utf-8'))
	print(content)

	cc=map(formatit,content)
	print(cc)

	cc=groupit(cc)
	with open('result.txt','w') as write:
		write.writelines(cc)
	write.close()

