'''
'''
import arcpy
import os

def FeatureDatasetProperty(desObject,isprint=True):
    if isprint:
        print(desObject.catalogPath)
    arcpy.env.workspace=desObject.catalogPath
    property={}
    property['name']=desObject.name
    property['dataType']=desObject.dataType
    fcnames=arcpy.ListFeatureClasses()
    print(fcnames)
    property['featureclassesCount']=len(fcnames)
    property['featureclasses']={}
    for fcname in fcnames:
        des=arcpy.Describe(desObject.catalogPath+'\\'+fcname)
        property['featureclasses'][fcname]=FeatureClassProperty(des,False)
    if isprint:
        print(property)
    return property

def RasterDatasetProperty(desObject,isprint=True):
    if isprint:
        print(desObject.catalogPath)
    property={}
    property['name']=desObject.name
    property['dataType']=desObject.dataType
    property['format']=desObject.format
    property['bandCount']=desObject.bandCount
    # raster band property
    # property['pixelType']=desObject.pixelType
    # property['height']=desObject.height
    # property['width']=desObject.width
    if isprint:
        print(property)
    return property

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
    property['table']=TableProperty(desObject,False)
    property['spatialReference']={}
    property['spatialReference']['name']=desObject.spatialReference.name
    property['spatialReference']['type']=desObject.spatialReference.type # Geographic/Projected
    property['spatialReference']['GCSname']=desObject.spatialReference.GCS.name
    property['spatialReference']['datumName']=desObject.spatialReference.datumName
    property['spatialReference']['spheroidName']=desObject.spatialReference.spheroidName
    if desObject.spatialReference.type=='Projected':
        property['spatialReference']['metersPerUnit']=desObject.spatialReference.metersPerUnit
    elif desObject.spatialReference.type=='Geographic':
        property['spatialReference']['metersPerUnit']=-1
    property['spatialReference']['linearUnitName']=desObject.spatialReference.linearUnitName # empty for GCS
    property['spatialReference']['angularUnitName']=desObject.spatialReference.angularUnitName # empty for PCS
    if isprint:
        print(property)
    return property

def TableProperty(desObject,isprint=True):
    if isprint:
        print(desObject.catalogPath)
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
    if isprint:
        print(property)
    return property

def RasterCatalogProperty(desObject,isprint=True):
    if isprint:
        print(desObject.catalogPath)
    property={}
    property['name']=desObject.name
    property['dataType']=desObject.dataType
    if isprint:
        print(property)
    return property

def ToolboxProperty(desObject,isprint=True):
    if isprint:
        print(desObject.catalogPath)
    property={}
    property['name']=desObject.name
    property['dataType']=desObject.dataType
    if isprint:
        print(property)
    return property

def ShapeFileProperty(desObject,isprint=True):
    if isprint:
        print(desObject.catalogPath)
    property=FeatureClassProperty(desObject,false)
    # property['name']=desObject.name
    # property['dataType']=desObject.dataType
    if isprint:
        print(property)
    return property

def CheckData(path):
    directory,basename=os.path.split(path)
    print('Location: '+directory+'   '+basename)
    format=''
    if len(basename.split('.'))>1:
        format=basename.split('.')[1]
    typefunc={'FeatureDataset':FeatureDatasetProperty,\
              'RasterDataset':RasterDatasetProperty,\
              'FeatureClass':FeatureClassProperty,\
              'Table':TableProperty,\
              'RasterCatalog':RasterCatalogProperty,\
              'Toolbox':ToolboxProperty,\
              'ShapeFile':ShapeFileProperty}

    desc=arcpy.Describe(path)
    if format=='gdb':# gdb
        arcpy.env.workspace=path
        # list all layers' attributes like feature, raster
        items=desc.children
        for item in items:
            # dataType:
            # FeatureDataset
            # RasterDataset
            # FeatureClass
            # Table
            # RasterCatalog
            # Toolbox
            # ShapeFile
            #print(item.name+':'+item.dataType)
            typefunc[item.dataType](item,True)
    else:# shapefile, rasterdataset layer
        arcpy.env.workspace=directory
        print(desc.dataType)
        typefunc[desc.dataType](desc)
    print('finish')
    

if __name__=='__main__':
    work=r'c:\py\database\DataTypes.gdb'
    # work='c:/py/database/sandiego.gdb/freeways'
    # work=r'c:\py\case\case1\april\apr.shp'# dataType=File/tx/mg
    # work=r'c:\py\database\tahoe\emer\erhill'
    CheckData(work)
