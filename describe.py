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
    property={}
    property['name']=desObject.name
    property['dataType']=desObject.dataType
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
            typefunc[item.dataType](item)
    else:# shapefile, rasterdataset layer
        typefunc[desc.dataType](desc)
    print('finish')
    

if __name__=='__main__':
    work=r'c:\py\database\DataTypes.gdb'
    # work=r'c:\py\case\case1\april\apr.shp'
    # work=r'c:\py\database\tahoe\emer\erhill'
    CheckData(work)
