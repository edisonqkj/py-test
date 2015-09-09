'''
	read python script file & run the script
'''
import os

print(os.getcwd())
f=open('describe.py','r')
content=f.read()
f.close()
print(content)
# exec(content)