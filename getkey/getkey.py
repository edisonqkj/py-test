'''
'''

import msvcrt
import arcpy
import multiprocessing

def getkey(mode=0):
	'''
		'a'  ->  97:   ord('a')
		97   ->  'a':  chr(97)
		mode:
		0  --  number[0-9]
		1  --  char[A-Z,a-z]
		2  --  string[0-9,A-Z,a-z]
	'''
	import random as rd
	print('Press:')
	while True:
		ch=msvcrt.getch()
		print('Key: {0}  Ascii: {1}'.format(ch,ord(ch)))
		# press Esc (27) to exit
		if ord(ch)==27:
			break
		if ch in ['a','w','d','s']:
			rdint=rd.randint(-10,10)
			return rdint
		if ord(ch) in range(48,58):
			return int(ch)

def update(inshp):
	# count=arcpy.GetCount_management(inshp)
	# print('count={0}'.format(count))

	des=arcpy.Describe(inshp)
	print('extent={0}'.format(des.extent))	
	xmin=des.extent.XMin
	ymin=des.extent.YMin
	xmax=des.extent.XMax
	ymax=des.extent.YMax

	rdint=getkey()
	start_x=(xmin+xmax)/2+100*rdint
	start_y=(ymin+ymax)/2+100*rdint
	print('start={0}'.format([start_x,start_y]))

	cur=arcpy.InsertCursor(inshp)
	row=cur.newRow()

	array=arcpy.Array()
	pt=arcpy.Point(start_x,start_y)
	array.add(pt)
	pt=arcpy.Point(start_x+3000,start_y)
	array.add(pt)
	pt=arcpy.Point(start_x+3000,start_y+2000)
	array.add(pt)
	pt=arcpy.Point(start_x,start_y+3000)
	array.add(pt)

	plg=arcpy.Polygon(array)
	row.setValue('Shape',plg)
	cur.insertRow(row)

	del cur

def showlist(mxd_path):
	mxd=arcpy.mapping.MapDocument(mxd_path)
	df=arcpy.mapping.ListDataFrames(mxd)[0]
	print(df.name)
	lyrs=arcpy.mapping.ListLayers(mxd, "", df)
	layer_datasource=[]
	layer_name=[]
	if len(lyrs)>0:
		print('Choose layer [id] to save shapes:')
		id=0
		for lyr in lyrs:
			layer_datasource.append(lyr.dataSource)
			layer_name.append(lyr.name)
			print('layer: {0}\t{1}\tid: {2}'.format(lyr.name,\
												   arcpy.Describe(lyr.dataSource).shapeType,\
												   id))
			id+=1
	layer_id=getkey()
	print('{0} is chosen'.format(layer_name[layer_id]))
	# interact to update shape
	update(layer_datasource[layer_id])

	mxd.activeView=df.name
	arcpy.RefreshActiveView()
	arcpy.RefreshTOC()

def add(mxd_path):
	mxd=arcpy.mapping.MapDocument(mxd_path)
	df=arcpy.mapping.ListDataFrames(mxd)[0]
	print(df.name)
	lyr=arcpy.mapping.ListLayers(mxd, "", df)[0]
	layer_datasource=[lyr.dataSource]
	layer_name=[lyr.name]
	# if len(lyrs)>0:
	# 	print('Choose layer [id] to save shapes:')
	# 	id=0
	# 	for lyr in lyrs:
	# 		layer_datasource.append(lyr.dataSource)
	# 		layer_name.append(lyr.name)
	# 		print('layer: {0}\t{1}\tid: {2}'.format(lyr.name,\
	# 											   arcpy.Describe(lyr.dataSource).shapeType,\
	# 											   id))
	# 		id+=1
	layer_id=0
	print('{0} is chosen'.format(layer_name[layer_id]))
	# interact to update shape
	update(layer_datasource[layer_id])
	# source_layer='C:/Users/Administrator/Desktop/py-test/Tracts.lyr'
	# arcpy.mapping.UpdateLayer(df,lyr,source_layer, symbology_only = True)
	# mxd.save()

def create(dirname):
	arcpy.env.workspace=dirname
	arcpy.env.overwriteOutput=True
	try:
		points = arcpy.CreateFeatureclass_management(dirname, "NewFeature", "Point")
		print("NewFeature is created")
		arcpy.AddField_management(points, "NewField", "TEXT", "", "", 20)
		print('NewField is added')
		# layer=arcpy.MakeFeatureLayer_management('NewFeature','layer')
	except arcpy.ExecuteError:
		print('Geoprocessing error:\n'+arcpy.GetMessages())
		arcpy.AddError('Geoprocessing error:\n'+arcpy.GetMessages())

if __name__=='__main__':
	# arcpy.ImportToolbox('C:\Users\Administrator\Desktop\py-test\key.tbx')
	import sys
	import os
	cwd=sys.path[0]+'/DataTypes.gdb'
	print(cwd)
	# create(cwd)
	mxd_path=arcpy.GetParameterAsText(0)
	mxd_path='C:/Users/Administrator/Desktop/2.mxd'
	# showlist(mxd_path)
	add(mxd_path)

	# import comtypes.client
	# # Load the required COM libraries  
	# esriFramework = comtypes.client.GetModule('C:/Program Files/ArcGIS/Desktop10.0/com/esriFramework.olb')  
	# esriArcMapUI = comtypes.client.GetModule('C:/Program Files/ArcGIS/Desktop10.0/com/esriArcMapUI.olb')  

	# # Get the current ArcMap session  
	# objApplication = comtypes.client.CreateObject(esriFramework.AppRef, interface=esriFramework.IApplication)  
	# objMxDocument = objApplication.Document.QueryInterface(esriArcMapUI.IMxDocument)  
	# objMxDocument.ActiveView.Refresh()
	# gp.addmessage("View refreshed...")
	# os.path.join(cwd,'1.mxd')
	
	# C:/Users/Administrator/Desktop/1.mxd
	# mxd=arcpy.mapping.MapDocument('CURRENT')
	# df=arcpy.mapping.ListDataFrames(mxd)[0]
	# print(df.name)
	# # table=arcpy.mapping.TableView('C:/Users/Administrator/Desktop/py-test/datatypes.gdb/DonutShops')
	# # arcpy.mapping.AddTableView(df,table)

	# # layer=os.path.join(cwd,'layer.lyr')
	# # layer=arcpy.mapping.Layer(layer)
	# # AUTO_ARRANGE, BOTTOM
	# # arcpy.mapping.AddLayer(df,layer,'AUTO_ARRANGE')
	# arcpy.RefreshActiveView()
	# arcpy.RefreshTOC()
	# # mxd.save()
	# del mxd





	# p=multiprocessing.Process(target=getkey)
	# p.start()
	# p.join()