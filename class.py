'''
'''

class Person:
	age=0
	def __init__(self,age):
		self.age=age
	def SayAge(self):
		print 'My age is',self.age
		
class Male(Person):
	gender='male'
	def SayGender(self):
		print 'My gender is',self.gender

a=Person(21)
a.SayAge()
b=Male(25)
b.SayAge()
b.SayGender()