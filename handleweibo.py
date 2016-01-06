# -*- coding: utf-8 -*-
'''
	handle weibo checkin raw data downloaded from github
'''

import os

def getCityCode(code_file):
	f=open(code_file,'r')
	raw_content=f.readlines()
	f.close()
	content=map(lambda line:line.strip('\n'),raw_content)
	out=os.path.dirname(code_file)+'/citycode.txt'
	f=open(out,'w')
	f.writelines(content)
	f.close()

	f=open(out,'r')
	content=f.readlines()
	f.close()
	# bug: output not utf-8
	# content='-'.join(content)
	print(content)

	# pattern
	import re
	# pattern=map(lambda line:re.findall(u'<p>.*^[<]</p>',line),content)
	pattern=re.findall(u'<p>(\w+)</p>',content)
	print(pattern)


def handle(csv):
	pass

if __name__=='__main__':
	code_file=ur'E:/ACTC/3-工作安排/课程/博士生课程/0-自然班/weibo/city.html'
	citycode=getCityCode(code_file)

	data_path=ur'E:/ACTC/3-工作安排/课程/博士生课程/0-自然班/weibo/WeiboDataShare-master'
	files=os.listdir(data_path)
	print(files)
	for f in files:
		handle(f)
	pass