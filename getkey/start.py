i=0
while True:
	i+=1
	arcpy.getkey()
	arcpy.RefreshActiveView()
	if i>2:break
