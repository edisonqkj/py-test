'''
'''
import arcpy
import os

def CreatePoint(pt):
	point=arcpy.Point(pt[0],pt[1])
	print('Create Point:{}'.format(point))
	return point

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
	return polyline

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
	print(type(geoobjlist)) # list
	area=0
	for obj in geoobjlist:
		area+=obj.area
		# print(obj.JSON)
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
	# print(plg.JSON)
	# point buffer
	arcpy.Buffer_analysis(geolist,outshp,'1000 feet')
	# polygon buffer
	arcpy.Buffer_analysis(plg,outshp+'plg','1000 feet')

def PointFeature(ptlist,outshp):
	# arcpy.CreateFeatureclass_management(outshp)
	geolist=[]
	for pt in ptlist:
		point=CreatePoint(pt)
		ptgeo=arcpy.PointGeometry(point)
		geolist.append(ptgeo)
		# print(ptgeo.JSON)
	arcpy.CopyFeatures_management(geolist,outshp)

def PrintPoint(inshp):
	g=arcpy.Geometry()
	geolist=arcpy.CopyFeatures_management(inshp,g)
	# print(g.count)
	print(geolist)
	# geilist --> [geometry objects]
	print('len(geolist)={}'.format(len(geolist)))
	i=0
	for geo in geolist:
		i+=1
		arrays=geo.getPart()
		print(geo.partCount)
		print('len(arrays)={}'.format(len(arrays)))
		# arrays
		j=0
		for array in arrays:
			j+=1
			# pt --> Point geomtry object
			print('len(array)={}'.format(len(array)))
			for k in range(array.count):
				pt=array.getObject(k)
				print('#{} shape #{} part #{} point: ({})'.format(i,j,k,pt))

def ReadPoint(inshp):
	cursor=arcpy.da.SearchCursor(inshp,['OID@','SHAPE@'])
	for row in cursor:
		ptgeometry=row[1]
		pt=ptgeometry.getPart()
		print('#{} feature: ({},{})'.format(row[0],pt.X,pt.Y))

def ReadPolylinePolygon(inshp):
	cursor=arcpy.da.SearchCursor(inshp,['OID@','SHAPE@','SHAPE@LENGTH'])
	for row in cursor:
		geometry=row[1]
		for i in range(geometry.partCount):
			array=geometry.getPart(i)
			j=0
			for pt in array:
				print('#{} feature,length={}, #{} part, #{} point: ({},{})'.format(row[0],row[2],i,j,pt.X,pt.Y))
				j+=1

def PointToPolygonBoundary(point,polygon,polyline):
	# link vertext to the points on the buffer boundary
	ptlist=arcpy.CopyFeatures_management(point,arcpy.Geometry())
	plglist=arcpy.CopyFeatures_management(polygon,arcpy.Geometry())
	dirname,basename=os.path.split(polyline)
	# des=arcpy.Describe(point)
	# fc=arcpy.CreateFeatureclass_management(dirname,basename,"Polyline","","","",des.spatialReference)
	# del des
	# cur=arcpy.InsertCursor(polyline)
	# each polygon concerning multiparts
	print('Polygon Count: {}'.format(len(plglist)))

	linelist=[]
	for pt in ptlist:
		# use getPart() method to get Point list from Geometry object
		# to PointGeometry, getPart() method returns a Point object
		# to Polygon, getPart() method returns an array of Array object,respectively corresponds to each part of the polygon feature
		point=pt.getPart()
		for plg in plglist:
			for part in plg.getPart():
				print('len(part)={}'.format(len(part)))
				for plgpt in part:
					# print(type(pt))
					array=arcpy.Array()
					array.add(point)
					array.add(plgpt)
					line=arcpy.Polyline(array)
					linelist.append(line)

					print('{} --> {}'.format(point,plgpt))
					# arcpy.Append_management(line,polyline,'NO_TEST')
					# print(line.getPart())

					# using insertcursor cautions: spatialreference
					# row=cur.newRow()
					# row.setValue('Shape',line)
					# cur.insertRow(row)
					# del array,line
	# del cur
	arcpy.CopyFeatures_management(linelist,polyline)
	del ptlist,plglist,linelist

def shift_features(in_features, x_shift=None, y_shift=None):
    """
    Shifts features by an x and/or y value. The shift values are in
    the units of the in_features coordinate system.
 
    Parameters:
    in_features: string
        An existing feature class or feature layer.  If using a
        feature layer with a selection, only the selected features
        will be modified.
 
    x_shift: float
        The distance the x coordinates will be shifted.
 
    y_shift: float
        The distance the y coordinates will be shifted.
    """
 
    with arcpy.da.UpdateCursor(in_features, ['SHAPE@XY']) as cursor:
        for row in cursor:
            cursor.updateRow([[row[0][0] + (x_shift or 0),
                               row[0][1] + (y_shift or 0)]])
 
    return
    
if __name__=='__main__':
	arcpy.env.overwriteOutput=True
	path='c:/py/database/sandiego.gdb/freeways'
	ptlist=[[1277000,344000],[1283000,344000],[1283000,336000]]
	buf='c:/py/database/datatypes.gdb/bufofpoints'
	bufplg=buf+'plg'
	# GeometryObject(path)
	# GeometryBuffer(ptlist,buf)
	plg='c:/py/database/datatypes.gdb/plgofpoints'
	# CreatePolygon(ptlist,plg)
	pt='c:/py/database/datatypes.gdb/points'
	# PointFeature(ptlist,pt)
	line='c:/py/database/datatypes.gdb/lines'
	PrintPoint(buf)
	# PointToPolygonBoundary(pt,bufplg,line)
	ReadPoint(pt)
	ReadPolylinePolygon(buf)