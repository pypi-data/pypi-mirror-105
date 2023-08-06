# -*- coding = -utf-8 -*-

# OOP.py
class Student:
	def __init__(self, name, lastname):
		self.name = name
		self.lastname = lastname
		self.exp = 0 # Experiment of Those Students
		self.lesson = 0 # Class Those Student ever learned
		self.vehicle = 'Bus'

	@property
	
	def fullname(self):
		return '{} {}'.format(self.name, self.lastname)

	def Coding(self):
		'''Coding == Computer Programming Class!'''
		self.AddEXP()
		
		print(f'{self.fullname} Is Learning Programming...')

	def ShowExp(self):
		print(f'{self.name} Got Experiment {self.exp} EXP (Learned {self.lesson} times)')

	def AddEXP(self):
		self.exp += 10
		self.lesson += 1

	def __str__(self):
		return self.fullname

	def __repr__(self):
		return self.fullname

	def __add__(self, other):
		return self.exp + other.exp

class Tesla():
	def __init__(self):
		self.model = 'Tesla Model S'

	def SelfDriving(self, st):
		print(f'Auto pilot on Enable!...Taking Mr. {st.name} back to home.')

	def __str__(self):
		return self.model

class SpecialStudent(Student):
	def __init__(self, name, lastname, father):
		super().__init__(name, lastname)
		self.father = father
		self.vehicle = Tesla()
		print(f'Do you know Who TF I AM!?... , My Father Name Is {self.father}.')

	def AddEXP(self):
		self.exp += 30
		self.lesson += 2

class Teacher:
	def __init__(self, fullname):
		self.fullname = fullname
		self.students = []

	def CheckStudent(self):
		for i, st in enumerate(self.students):
			print(f"---- **Student of Teacher's {self.fullname}** ----\n")
			print(f'{i+1}--->{st.fullname} [{st.exp} EXP][Learned {st.lesson} times].\n')


	def AddStudent(self, st):
		self.students.append(st)


if __name__ == '__main__':
	# Day 0
	allstudent = []

	teacher1 = Teacher('Ada')
	teacher2 = Teacher('Bill Gates')
	print(teacher1.students)


	# Day 1
	print('--- Day 1 ---') 
	st1 = Student('PonAek', 'JanOCha')
	allstudent.append(st1) # Register Finished then Save to List! Immediately
	print(st1.fullname)
	teacher2.AddStudent(st1)


	# Day 2
	print('--- Day 2 ---')
	st2 = Student('steve', 'Jobs')
	allstudent.append(st2)
	print(st2.fullname)
	teacher2.AddStudent(st2)


	# Day 3
	print('--- Day 3 ---')
	for i in range(3):
		st1.Coding()
	st2.Coding()
	st1.ShowExp()
	st2.ShowExp()

	# Day 4
	print('--- Day 4 ---')

	stp1 = SpecialStudent('Def', 'Editor', 'Pychoom')
	allstudent.append(stp1)
	print(stp1.fullname)
	print('Teacher, Can I take free some 20 exp')
	stp1.exp = 20 # Can edit values in Class
	stp1.Coding()
	stp1.ShowExp()
	teacher1.AddStudent(stp1)

	# Day 5
	print('--- Day 5 ---')
	print('Student How can you back to home?')
	print(allstudent)

	for st in allstudent:
		print(f'Me, {st.name} Back to home by {st.vehicle}.')
		if isinstance(st, SpecialStudent):
			st.vehicle.SelfDriving(st)

	# Day 6
	print('--- Day 6 ---')

	teacher1.CheckStudent()
	teacher2.CheckStudent()

	print('All Scores of Two Studet', st1+st2)