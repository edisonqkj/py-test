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
	return head+result+'\n'

def groupit(strs):
	# A\nB\nC\nD --> A\nB\n+\n\n+C\nD\n+\n\n
	# add a new line in every 5 rows
	# res=[i+'\n' if i%2==0 for i in strs]
	# result=[i+'\n\n\n' if i%10==0 for i in res]
	# [i if i>2 else i-1 for i in a]
	result=[]
	for index,item in enumerate(strs):
		result.append(item)
		if (index+1)%10==0:
			result.append('\n\n\n')

	# n=str.strip('\n')
	# n=n.strip(',')
	# sub=n.split(',')
	# res=[]
	# for i in range(1,len(sub)+1):
	# 	if i % 2==1:
	# 		res.append(sub[i-1]+'('+sub[i]+')')
	# result=' -> '.join(res)+'\n'
	return result

def gettoolname(str):
	cnen=str.split('\n')[0].strip(')').split('(')
	cn=cnen[0]
	en=cnen[1]
	return cn.lower()+'\n'+en.lower()+'\n'

if __name__ == '__main__':
	f=u'tool.csv'
	csv=open(f,'r')
	csv.readline()
	content=csv.readlines()
	csv.close()
	# print(','.join(content).encode('utf-8'))
	print 'CONTENT:\n',content

	cc=map(formatit,content)
	print 'PATH:\n',cc
	
	tool=map(gettoolname,cc)
	print 'TOOL:\n',tool

	gptool=groupit(tool)
	with open('tools.txt','w') as write1:
		write1.writelines(gptool)
	write1.close()
	print 'written finished.'

	gpcc=groupit(cc)
	with open('result.txt','w') as write2:
		write2.writelines(gpcc)
	write2.close()
	print 'written finished.'
