'''
'''
import arcpy
import os

def ListWalk(path):
	for root,dirs,files in os.walk(path):
		print root,dirs,files

def ListWorkspace(path):
	arcpy.env.workspace=path;
	workspace_type=['Access','Coverage','FileGDB','Folder','SDE','All']
	gdb=arcpy.ListWorkspaces('*','FileGDB')
	print(gdb)

def ListDataset(path):
	arcpy.env.workspace=path;
	dataset_type=['Coverage','Feature','GeometricNetwork','Mosaic','Network',\
				  'ParcelFabric','Raster','RasterCatalog','Schematic',\
				  'Terrain','Tin','Topology','All']
	ds=arcpy.ListDatasets('*','Raster')
	print(ds)

def ListFeatureClass(path):
	arcpy.env.workspace=path;
	fc_type=['Annotation','Arc','Dimension','Edge','Junction','Label' \
			 'Line','Multipatch','Node','Point','Polygon','Polyline',\
			 'Region','Route','Tic','All']
	fc=arcpy.ListFeatureClasses('*','All')
	print(fc)
	return fc

def ListField(path):
	directory,dataset=os.path.split(path)
	arcpy.env.workspace=directory;
	fld_type=['BLOB','Date','Double','Geometry','GlobalID','GUID' \
			 'Integer','OID','Raster','Single','SmallInteger','String','All']
	flds=arcpy.ListFields(dataset,'*','All')
	fldname=[]
	for fld in flds:
		print(fld.name)
		fldname.append(fld.name)
	return fldname

def ListRaster(path):
	arcpy.env.workspace=path;
	raster_type=['BMP','GIF','IMG','JP2','JPG','PNG','TIF','GRID','All']
	raster=arcpy.ListRasters('*','All')
	print(raster)

def ListTable(path):
	arcpy.env.workspace=path;
	table_type=['dBASE','INFO','All']
	table=arcpy.ListTables('*','All')
	print(table)

def ListFile(path):
	arcpy.env.workspace=path;
	files=arcpy.ListFiles('*.shp')	# *.txt
	print(files)

def ListIndex(path):
	directory,dataset=os.path.split(path)
	arcpy.env.workspace=directory;
	indexes=arcpy.ListIndexes(dataset)
	for index in indexes:
		print(index.name)

def ListVersion(path):
	# sde version
	pass

if __name__=='__main__':
	work='c:/py/database/tahoe/'
	# ListWalk(work)
	work='c:/py/database/'
	# ListWorkspace(work)
	work='c:/py/database/DataTypes.gdb'
	# print(os.path.splitext(work))
	# ListDataset(work)
	# ListFeatureClass(work)
	# ListRaster(work)
	# ListTable(work)
	work='c:/py/database/DataTypes.gdb/parcels'
	# ListField(work)
	# ListIndex(work)
	work='c:/py/case/case1/april/'	# Apr.shp
	# ListFile(work)