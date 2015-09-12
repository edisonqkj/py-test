# -*- coding:gb2312 -*-
import os,sys,arcpy
# txt format
# 1,,@
# J1,4167184.773,39430247.257
# J2,4167167.360,39430327.747
# 2,,@
# J3,4167184.773,39430247.257
# J4,4167167.360,39430327.747
#解析坐标文件
filename="此处填写txt文件的完整目录"
coordfile=open(filename)
i=0
coordList=[]
polygonCoordList=[]
startX,startY=0.0,0.0
for line in coordfile.readlines():
    i+=1
    print "正在读取:",line
    if i<1 or line[-2]=="@":
        continue
    Y,X=map(lambda x:float(x),line.split(",")[2:4])
    if startX==0 and startY==0:
        startX,startY=X,Y
        polygonCoordList.append([X,Y])
        continue
        
    if startX !=X and startY !=Y:
        polygonCoordList.append([X,Y])
    else:
        startX,startY=0,0
        coordList.append(polygonCoordList)
        polygonCoordList=[]
coordfile.close()

#生成多边形
ii=0
point=arcpy.Point()
array=arcpy.Array()
featureList=[]
for polygon in coordList:
    ii+=1
    print "====第%s个多边形===="%ii
    for coordPair in polygon:
        print "x:{0}    y:{1}".format(coordPair[0],coordPair[1])
        point.X=coordPair[0]
        point.Y=coordPair[1]
        array.add(point)
    array.add(array.getObject(0))
    polygongeo=arcpy.Polygon(array)
    array.removeAll()
    featureList.append(polygongeo)

#开始复制要素
arcpy.env.overWriteOutput=True
out_feature_class="./%s.shp"%os.path.splitext(os.path.basename(filename))[0]
arcpy.CopyFeatures_management(featureList,out_feature_class)
print "====Well done===="    
del point
del array
del featureList

input()
