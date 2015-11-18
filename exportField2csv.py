'''
	Export All the Fields' Attributes into CSV File
	Attributes:
			-	Field Name
			-	Field Type
'''
import arcpy
import os
import sys

def TableProperty(desObject):
	print('Path: '+desObject.catalogPath)
	property={}
	property['name']=desObject.name
	property['dataType']=desObject.dataType
	property['hasOID']=desObject.hasOID
	property['OIDFieldName']=desObject.OIDFieldName
	property['fields']={}
	for field in desObject.fields:
		property['fields'][field.name]=[field.type,field.length]
	property['indexes']=[]
	for index in desObject.indexes:
		property['indexes'].append(index.name)
	print('Read shapefile table is finished.')
	return property

def Run(shp,csv):
	desc=arcpy.Describe(shp)
	property=TableProperty(desc)
	print(property)
	f=open(csv,'w')
	for fname in property['fields']:
		ftype=property['fields'][fname][0]
		record=','.join([fname,ftype,'\n'])
		f.write(record)
		print(record)
	f.close()
	print('Exportation is finished.')

if __name__=='__main__':
	shp='c:/py/database/sandiego.gdb/freeways'
	csv='result.csv'
	Run(shp,csv)