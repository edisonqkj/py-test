'''
'''
import arcpy
import os

def CreatePoint(pt):
	point=arcpy.Point(pt[0],pt[1])
	print('Create Point:{}'.format(point))

def CreateMultiPoint(ptlist):
	array=arcpy.Array()
	for pt in ptlist:
		point=arcpy.Point(pt[0],pt[1])
		array.add(point)
	multipoint=arcpy.MultiPoint(array)
	print('Create MultiPoint:{}'.format(multipoint))

def CreatePoyline(ptlist):
	array=arcpy.Array()
	for pt in ptlist:
		point=arcpy.Point(pt[0],pt[1])
		array.add(point)
	polyline=arcpy.Polyline(array)
	print('Create Polyline:{}'.format(polyline))

def CreatePolygon(ptlist,outshp):
	array=arcpy.Array()
	for pt in ptlist:
		point=arcpy.Point(pt[0],pt[1])
		array.add(point)
	polygon=arcpy.Polygon(array)
	arcpy.CopyFeatures_management(polygon,outshp)
	print('Create Polygon:{}'.format(polygon))

def GeometryObject(inshp):
	feature=os.path.basename(inshp)
	count=arcpy.GetCount_management(inshp)
	print('{} has {} features'.format(feature,count))

	g=arcpy.Geometry()# empty geometry object
	geoobjlist=arcpy.Buffer_analysis(inshp,g,'100 meters')
	area=0
	for obj in geoobjlist:
		area+=obj.area
	print('{}\'s total Area= {}'.format(feature,area))

def GeometryBuffer(ptlist,outshp):
	basename=os.path.basename(outshp)
	geolist=[]
	array=arcpy.Array()
	for pt in ptlist:
		point=arcpy.Point(pt[0],pt[1])
		ptgeo=arcpy.PointGeometry(point)
		geolist.append(ptgeo)
		array.add(point)
	plg=arcpy.Polygon(array)
	arcpy.Buffer_analysis(plg,outshp,'1000 feet')

if __name__=='__main__':
	arcpy.env.overwrite=True
	path='c:/py/database/sandiego.gdb/freeways'
	ptlist=[[1277000,344000],[1283000,344000],[1283000,336000]]
	outshp='c:/py/database/datatypes.gdb/bufofpoints1'
	GeometryObject(path)
	GeometryBuffer(ptlist,outshp)
	CreatePolygon(ptlist,outshp+'1')