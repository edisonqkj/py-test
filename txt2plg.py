import arcpy,fileinput,os
from arcpy import env
env.overwriteOutput=True
infile="point.txt"
# 0 118.5 38.9
# 1 117.1 38.1
# 2 116.9 38.9
# 3 118.5 41.0
# 0 118.5 38.9
fc="new.shp"
dataset="lines.shp"
spatial_ref=arcpy.Describe(dataset).spatialReference
arcpy.CreateFeatureclass_management('./',fc,"Polygon")#,spatial_reference=spatial_ref)
cursor=arcpy.InsertCursor(fc)#,["SHAPE@"])
row=cursor.newRow() 
array=arcpy.Array()
array1=arcpy.Array()

f=open(infile,'r')
for line in f.readlines():
	ele=line.strip('\n').split(' ')
	print(ele)
	point=arcpy.Point(float(ele[1]),float(ele[2]))
	print(point)
	array.add(point)
f.close()

polygon=arcpy.Polygon(array)
array.removeAll()
row.shape=polygon
cursor.insertRow(row)

del row
del cursor
