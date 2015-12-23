# -*- coding: utf-8 -*-
'''
	Format string into specific structure
	Chinese character is supported
'''
import os

def formatit(str):
	# A,B,C,D  -->  A(B) -> C(D)
	n=str.strip('\n')
	n=n.strip(',')
	sub=n.split(',')
	res=[]
	for i in range(1,len(sub)+1):
		if i % 2==1:
			res.append(sub[i-1]+'('+sub[i]+')')
	result=' -> '.join(res)+'\n'
	return result

if __name__ == '__main__':
	f=u'E:/ACTC/0-Weixin/ArcToolbox工具列表.csv'
	csv=open(f,'r')
	csv.readline()
	content=csv.readlines()
	csv.close()
	# print(','.join(content).encode('utf-8'))
	print(content)
	cc=map(formatit,content)
	print(cc)
	with open('result.txt','w') as write:
		write.writelines(cc)
	write.close()

