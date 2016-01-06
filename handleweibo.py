# -*- coding: utf-8 -*-
'''
	handle weibo checkin raw data downloaded from github
'''

import os
import arcpy

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

def isDigitOrFloat(str):
	# int
	if str.isdigit():
		return True
	else:# float
		try: 
			float(str)
			return True
		except(ValueError): 
			return False

		# if str.isalpha():# all character
		# 	return False
		# if str.isalnum():# character & number
		# 	return False
		# # if type(eval(str))==float:
		# # 	return True
		# parts=str.split('.')
		# if len(parts)!=2:
		# 	return False
		# if parts[0].isdigit() or parts[1].isdigit():
		# 	return True
		# return True

def handle(csv):
	# structure:
	# poiid,title,address,lon,lat,city,category_name,checkin_num,photo_num
	# some error occure in splitting string line as more comma is in title & address
	# for the sake of creating points, here goes to extract lon & lat instead
	# of all the attributes.
	print(csv)
	checkin_points=[]
	f=open(csv,'r')
	content=f.readlines()
	f.close()
	# print(content[0])
	# print(content[1])
	for line in content:
		line=line.strip('\n')
		items=line.split(',')
		# print(items[3])
		if isDigitOrFloat(items[3]):
			checkin_points.append({'lon':items[3],'lat':items[4]})
		else:
			i=1
			while(not isDigitOrFloat(items[3+i])):
				i=i+1
			checkin_points.append({'lon':items[3+i],'lat':items[4+i]})
		# checkin_points.append({'poiid':items[0],\
		# 					   'title':items[1],\
		# 					   'address':items[2],\
		# 					   'lon':items[3],\
		# 					   'lat':items[4],\
		# 					   'city':items[5],\
		# 					   'category_name':items[6],\
		# 					   'checkin_num':items[7],\
		# 					   'photo_num':items[8]})
	print(checkin_points[:5])
	return checkin_points

def toShapefile(records,outshp):
	points=[]
	for record in records:
		print(record)
		pt=arcpy.Point()
		pt.X=record['lon']
		pt.Y=record['lat']
		point=arcpy.PointGeometry(pt)
		points.append(point)
	arcpy.CopyFeatures_management(points,outshp)

def toText(records,outtxt):
	with open(outtxt,'w') as write:
		for record in records: 
			print(record)
			write.write(record['lon']+','+record['lat']+'\n')
	write.close()

if __name__=='__main__':
	code_file=ur'city.html'
	# citycode=getCityCode(code_file)

	data_path=ur'weibo'
	files=os.listdir(data_path)
	print(files)
	for f in files:
		if f[-3:]=='csv' and f=='aomen.csv':
			records=handle(os.path.join(data_path,f))
			# toShapefile(records,os.path.join(data_path,'points.shp'))
			toText(records,os.path.join(data_path,'points.txt'))