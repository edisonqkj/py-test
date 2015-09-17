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

if __name__=='__main__':
	inshp='c:/py/database/datatypes.gdb/bufofpoints'
	MakeFeatureLayer(inshp)