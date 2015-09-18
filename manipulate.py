'''
'''
import arcpy
import os

def MakeFeatureLayer(inshp):
	layer='layer'
	field='orig_fid'
	arcpy.env.workspace=os.path.dirname(inshp)
	newfield=arcpy.AddFieldDelimiters(arcpy.env.workspace,field)
	sql=newfield+'>1'
	print(sql)
	fieldinfo=arcpy.FieldInfo()
	fieldinfo.addField('BUFF_DIST','dist','visible','')
	fieldinfo.addField('ORIG_FID','oid','hidden','')

	arcpy.MakeFeatureLayer_management(inshp,layer,sql,'',fieldinfo)
	count=arcpy.GetCount_management(layer)
	print('{}: {}'.format(sql,count))

	arcpy.CopyFeatures_management(layer,'layershp')

def function():
	arcpy.env.workspace='c:/py/database/corvallis.gdb'
	fld='PARK_NAME'
	nameFld=arcpy.AddFieldDelimiters('Parks',fld)
	value='Central Park'
	sql=nameFld+" = '"+ value+"'"
	arcpy.MakeFeatureLayer_management('Parks',value,sql)
	count=arcpy.GetCount_management(value)
	print(count)

	fldinfo=arcpy.FieldInfo()
	fldinfo.addField('RECCFLAG','','HIDDEN','')
	fldinfo.addField('RECAFLAG','','HIDDEN','')
	fldinfo.addField('METER_NUM','METERNUM','VISIBLE','')
	arcpy.MakeFeatureLayer_management('ParkingMeters','Meters','','',fldinfo)
	count=arcpy.GetCount_management('Meters')
	print(count)

	selectfeature=value
	relation='WITHIN_A_DISTANCE'
	distance='500 feet'
	selecttype='NEW_SELECTION'
	arcpy.SelectLayerByLocation_management('Meters',relation,selectfeature,distance,selecttype)
	count=arcpy.GetCount_management('Meters')
	print(count)
	arcpy.CopyFeatures_management('Meters','centralparkmeters')


if __name__=='__main__':
	inshp='c:/py/database/datatypes.gdb/bufofpoints'
	# MakeFeatureLayer(inshp)
	function()