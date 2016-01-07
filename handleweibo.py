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
	# print(csv)
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
		if len(items)<5:
			continue
		if isLonLat(items[3],items[4]):
			checkin_points.append({'poiid':items[0],'lon':items[3],'lat':items[4]})
		else:
			for i in range(0,len(items)-1):
				if isLonLat(items[i],items[i+1]):
					checkin_points.append({'poiid':items[0],'lon':items[i],'lat':items[i+1]})
					break
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

def isLonLat(lonstr,latstr):
	# China:
	# longitude:	73-135
	# latitude:		18-54(exclude south China ocean)
	if isDigitOrFloat(lonstr) and float(lonstr)<=180 and float(lonstr)>=73 \
		and isDigitOrFloat(latstr) and float(latstr)<=54 and float(latstr)>=18:
		return True
	return False

def toShapefile(records,outshp):
	# print(outshp)
	points=[]
	for record in records:
		# print(record)
		pt=arcpy.Point()
		pt.X=float(record['lon'])
		pt.Y=float(record['lat'])
		point=arcpy.PointGeometry(pt)
		points.append(point)
	arcpy.env.overwriteOutput=True
	arcpy.CopyFeatures_management(points,outshp)
	print('shapefile is saved.')

def toText(records,outtxt):
	with open(outtxt,'w') as write:
		write.write('lon,lat,poiid\n')
		for record in records: 
			print(record)
			write.write(record['lon']+','+record['lat']+','+record['poiid']+'\n')
	write.close()

if __name__=='__main__':
	code_file=ur'city.html'
	# citycode=getCityCode(code_file)

	data_path=ur'E:/ACTC/3-工作安排/课程/博士生课程/0-自然班/weibo/WeiboDataShare-master'
	points=[]
	files=os.listdir(data_path)
	print(files)
	for f in files:
		if f[-3:]=='csv' and f[0:2]!='0-' and f=='beijing.csv':
			if(os.path.exists(os.path.join(data_path,f[:-4]+'.shp'))):
				continue
			records=handle(os.path.join(data_path,f))
			if len(records)==0:
				continue
			# points.extend(records)
			# toShapefile(records,os.path.join(data_path,f[:-4]+'.shp'))
			toText(records,os.path.join(data_path,f[:-4]+'_xyid.csv'))
	# toText(points,os.path.join(data_path,'0-points.csv'))