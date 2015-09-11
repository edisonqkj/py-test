'''
'''
import os
import sys
from list import ListFeatureClass,ListField
from describe import FeatureClassProperty

def Search(object):
	fldname=ListField(object)
	print(fldname)
	cursor=arcpy.SearchCursor(object,fields=fldname[0]+';'+fldname[1])
	for row in cursor:
		# cmd="row."+fldname[0]
		# print(eval(cmd))
		print(row.getValue(fldname[0]))
	del row,cursor

def Update(object):
	fldname=ListField(object)
	print(fldname)
	cursor=arcpy.UpdateCursor(object)
	for row in cursor:
		if row.getValue('RECORD_ID') % 2==0:
			row.setValue('SUMLEV',999)
			cursor.updateRow(row)
	del row,cursor

def Insert(object):
	fldname=ListField(object)
	print(fldname)
	cursor=arcpy.InsertCursor(object)
	row=cursor.newRow()
	row.setValue('RECORD_ID',123456)
	cursor.insertRow(row)
	del row,cursor

def Geometry(object):
	fc=arcpy.Describe(object)
	property=FeatureClassProperty(fc,False)#True
	shapeType=property['shapeType']
	if shapeType <> 'Point':
		cursor=arcpy.SearchCursor(object)
		area=0
		length=0
		for row in cursor:
			# a record with empty shape
			if row.Shape <> None:
				if shapeType=='Polygon':
					area+=row.Shape.area
				# elif shapeType=='Polyline':
				length+=row.Shape.length
			# print('Centroid:({},{})'.format(row.Shape.centroid.X,row.Shape.centroid.Y))
		if shapeType=='Polygon':
			print('{}\'s Sum Area= {}'.format(fc.name,area))
		# if shapeType=='Polyline':
		print('{}\'s Sum Length= {}'.format(fc.name,length))

		del cursor,row
	else:
		print('{0}: shapeType={1}'.format(fc.name,property['shapeType']))
	del property,fc

def Project(object):
	fc=arcpy.Describe(object)
	print('{}\'s spatial reference: {}'.format(fc.name,fc.spatialReference.name))
	prj='C:/py/Database/Mercator (world).prj'
	Mercator=arcpy.SpatialReference(prj)
	cursor=arcpy.SearchCursor(object)
	cursor1=arcpy.SearchCursor(object,spatial_reference=Mercator)
	row=cursor.next()
	row1=cursor1.next()
	print('{}: centroid.X= {}'.format(fc.spatialReference.name,row.Shape.centroid.X))
	print('{}: centroid.X= {}'.format(Mercator.name,row1.Shape.centroid.X))
	del fc,cursor,cursor1,row,row1,Mercator

if __name__=='__main__':
	work='c:/py/database/DataTypes.gdb'
	fcs=ListFeatureClass(work)
	print(fcs)
	for fc in fcs: 
		# Search(work+'/'+fc)
		# Geometry(os.path.join(work,fc))
		Project(os.path.join(work,fc))
		# break
	# Update(work+'/'+'updatefc')
	# Insert(work+'/'+'updatefc')
	