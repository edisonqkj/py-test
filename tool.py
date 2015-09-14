'''
'''
import os
import arcpy

def FeatureClassProperty(desObject,isprint=True):
    if isprint:
        print(desObject.catalogPath)
    property={}
    property['name']=desObject.name
    property['dataType']=desObject.dataType
    property['featureType']=desObject.featureType
    property['hasM']=desObject.hasM
    property['hasZ']=desObject.hasZ
    property['hasSpatialIndex']=desObject.hasSpatialIndex
    property['shapeFieldName']=desObject.shapeFieldName
    property['shapeType']=desObject.shapeType
    # property['table']=TableProperty(desObject,False)
    # property['spatialReference']={}
    # property['spatialReference']['name']=desObject.spatialReference.name
    # property['spatialReference']['type']=desObject.spatialReference.type
    # property['spatialReference']['GCSname']=desObject.spatialReference.GCS.name
    # property['spatialReference']['datumName']=desObject.spatialReference.datumName
    # property['spatialReference']['spheroidName']=desObject.spatialReference.spheroidName
    if isprint:
        print(property)
    return property

def Geometry(object):
	fc=arcpy.Describe(object)
	property=FeatureClassProperty(fc,False)#True
	shapeType=property['shapeType']

	result=''
	if shapeType <> 'Point':
		cursor=arcpy.SearchCursor(object)
		area=0
		length=0
		i=0
		for row in cursor:
			i+=1
			arcpy.AddMessage('#{} shape: {}'.format(i,shapeType))
			# a record with empty shape
			if row.Shape <> None:
				if shapeType=='Polygon':
					area+=row.Shape.area
				# elif shapeType=='Polyline':
				length+=row.Shape.length
			# print('Centroid:({},{})'.format(row.Shape.centroid.X,row.Shape.centroid.Y))
			arcpy.AddMessage('Centroid:({},{})'.format(row.Shape.centroid.X,row.Shape.centroid.Y))
			arcpy.AddMessage('Xmin={},Xmax={})'.format(row.Shape.extent.XMin,row.Shape.extent.XMax))
		if shapeType=='Polygon':
			print('{}\'s Sum Area= {}'.format(fc.name,area))
			result+='{}\'s Sum Area= {}\n'.format(fc.name,area)
		# if shapeType=='Polyline':
		print('{}\'s Sum Length= {}'.format(fc.name,length))
		result+='{}\'s Sum Length= {}\n'.format(fc.name,length)
		del cursor,row
	else:
		print('{0}: shapeType={1}'.format(fc.name,property['shapeType']))
		result+='{0}: shapeType={1}\n'.format(fc.name,property['shapeType'])
	del property,fc
	return result

if __name__=='__main__':
	path=arcpy.GetParameterAsText(0); # set parameter's property [MultiValue]=Yes
	shapetype=arcpy.GetParameterAsText(1); # [MultiValue]=Yes
	field=arcpy.GetParameterAsText(2);
	fpath=arcpy.GetParameterAsText(3);
	arcpy.AddMessage(path)
	arcpy.AddMessage(shapetype)
	fcs=path.split(';')
	f=open(fpath,'w')
	for fc in fcs:
		res=Geometry(fc)
		arcpy.AddMessage(res)
		f.writelines(res)
	f.close()