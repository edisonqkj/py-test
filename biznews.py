'''
## Download all jpgs on http://www.talkingbiznews.com/wp-content/uploads/
## .../uploads/year/month/*.jpg
## Time: 5/9/14
## Author: Edison Qian
## E-mail: edison90110@gmail.com
'''
from __future__ import print_function
import os
import datetime
import time
import functools

def time_me(info="Used"):
	# not work
	def _time_me(fn):
		@functools.wraps(fn)
		def _wrapper(*args, **kwargs):
			start = time.clock()
			fn(*args, **kwargs)
			print("%s %s %s" % (fn.__name__, info, time.clock() - start), "second")
		return _wrapper
	return _time_me

def getImageUrls(dir):
	# under the given directory
	# images are saved in each year & month
	print("Current directory: "+dir)
	makeDir(dir)
	if os.path.exists(dir+"urls.txt"):
		f=open(dir+"urls.txt")
		imgurls=f.readlines()
		f.close()
		print(dir+"urls.txt")
		return imgurls

	url='http://www.talkingbiznews.com/wp-content/uploads/'

	start_time=datetime.datetime.now()

	# [DIR]-year
	years=getDirList(url)
	print("Year list: ")
	print(years)
	# make year dirs
	map(lambda year:makeDir(dir+year),years)

	costtime=(datetime.datetime.now()-start_time).seconds
	print('cost: '+str(costtime)+'s')
	start_time=datetime.datetime.now()

	# [DIR]-month
	months=map(lambda year:getDirList(url+year+"/"),years)
	print("Month list: ")
	print(months)
	# make month dirs
	map(lambda year,mlist:\
		map(lambda month:\
			makeDir(dir+year+"/"+month+"/"),\
			mlist),years,months)

	costtime=(datetime.datetime.now()-start_time).seconds
	print('cost: '+str(costtime)+'s')
	start_time=datetime.datetime.now()

	# [IMG]-jpgs
	images=map(lambda year,mlist:\
				map(lambda month:\
						getImageList(url+year+"/"+month),\
						mlist),years,months)
	# images=map(lambda month:getImageList(url+years[-1]+"/"+month),months[-1])
	print("Image Name list: ")
	# print(images)
	costtime=(datetime.datetime.now()-start_time).seconds
	print('cost: '+str(costtime)+'s')
	start_time=datetime.datetime.now()

	# get images' urls
	imgurls=[]
	map(lambda year,mlist,ilists:\
			map(lambda month,ilist:\
				map(lambda img:\
					imgurls.append(url+year+"/"+month+"/"+img),\
					ilist),\
				mlist,ilists),\
			years,months,images)
	print("Image Url list: ")
	# print(imgurls)
	costtime=(datetime.datetime.now()-start_time).seconds
	print('cost: '+str(costtime)+'s')

	# save urls into urls.txt
	print("Writing into file: ")
	writeImagesUrls(dir+"urls.txt",imgurls)

	return imgurls

def makeDir(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)
	else:
		# here are codes for clearing files
		pass

def writeImagesUrls(path,urls):
	# ['.../2010/01/a.jpg','.../2010/01/b.jpg']
	print(path)
	f=open(path,"w")
	for url in urls:
		f.writelines(url+'\n')
		print("Written: "+url)
	f.close()

# @time_me
def getDirList(url):
	# ...href="2010/... -> '2010'
	# ...href="01/... -> '01'
	import urllib
	wp = urllib.urlopen(url)
	content = wp.read().split('\n')
	import re
	digits=map(lambda line:re.findall("href=\"(\d+)",line),content)
	# [[],['2010'],['2011']] -> ['2010','2011']
	return sum(digits,[])

# @time_me
def getImageList(url):
	# ...href="abc.jpg" -> "abc.jpg"
	import urllib
	wp = urllib.urlopen(url)
	content = wp.read().split('\n')
	import re
	digits=map(lambda line:re.findall("href=\"(.*?\.jpg)\"",line),content)
	# [[],['abc.jpg'],['def.jpg']] -> ['abc.jpg','def.jpg']
	return sum(digits,[])

# @time_me
def downloadImages(dir,url):
	# dir=current directory
	# url='.../uploads/2010/01/abc.jpg'
	# save to dir/2010/01/abc.jpg
	import urllib
	outputFile=dir+'/'.join(url.split('/')[-3:])
	# download image
	if not os.path.exists(outputFile):
		urllib.urlretrieve(url, outputFile)

	size=1.0*os.path.getsize(outputFile)/1024**2# Megabyte
	return outputFile,str(size)

if __name__=='__main__':
	save_dir,runfile=os.path.split(os.path.realpath(__file__))
	print(save_dir,runfile)
	dir=save_dir+"zzz/"

	print("Start...")
	start_time=datetime.datetime.now()
	# 1.get Image urls
	imgurls=getImageUrls(dir)

	costtime4urls=(datetime.datetime.now()-start_time).seconds
	print('GetImageUrls cost: '+str(costtime4urls)+'s')
	
	# 2.download each image
	for url in imgurls:
		each_time=datetime.datetime.now()

		output,size=downloadImages(dir,url)

		eachcost=(datetime.datetime.now()-each_time).seconds
		print("Saved: "+output+\
			'\tSize: '+str(size)+'M'+\
			'\tCost: '+str(eachcost)+'s')
	allcost=(datetime.datetime.now()-start_time).seconds
	print("All cost: "+str(allcost)+'s')
