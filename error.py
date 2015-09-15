'''
'''
import os
import arcpy

def tryexcept():
	try:
		print('try-except')
		a=[1,2]
		# raise Exception
		for i in range(3):
			print('a[{}]={}'.format(i,a[i]))
		# raise NameError('name is error')
	except:
		print('this except block')

def exception():
	try:
		print('exception')
		a=[1,2]
		for i in range(3):
			print('a[{}]={}'.format(i,a[i]))
	except Exception as e:
		print('Error: '+str(e))

def execeuteerror():
	try:
		print('execeute-error')
		a=[1,2]
		for i in range(3):
			if i<2:
				print('a[{}]={}'.format(i,a[i]))
			else:
				pass
				# arcpy.AddError('i={}'.format(i))
				# arcpy.Buffer_analysis('')
	except arcpy.ExecuteError:
		print('Geoprocessing error:\n'+arcpy.GetMessages())
		arcpy.AddMessage('Geoprocessing error:\n'+arcpy.GetMessages())
		arcpy.AddError('Geoprocessing error:\n'+arcpy.GetMessages())
		print('Add processing code here:\n')

def traceback():
	try:
		print('traceback')
		a=[1,2]
		for i in range(3):
			print('a[{}]={}'.format(i,a[i]))
		arcpy.Buffer_analysis('')
	except:
		import sys
		tb=sys.exc_info()[2]
		# tbinfo=traceback.format_tb(tb)[0]

		pymsg='Python error:\n'+str(sys.exc_info()[1])
		msgs='Arcpy error:\n'+arcpy.GetMessages(2)
		arcpy.AddError(pymsg)
		arcpy.AddError(msgs)

		print(pymsg+'\n')
		print(msgs)

if __name__=='__main__':
	tryexcept()
	exception()
	execeuteerror()
	traceback()