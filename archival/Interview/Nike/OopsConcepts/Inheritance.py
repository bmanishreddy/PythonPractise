class Employee:

    def __init__(self,name,age,exp,salary):
        #initate the atributes for the constructor
        self.name = name
        self.age = age
        self.exp = exp
        self.salary = salary

    #Methord to show details of the employees
    def show(self):
        print("Details from Employee Class",self.name,self.age,self.exp,self.salary)

class Engineers(Employee):

    def __init__(self,name,age,exp,salary,level):
        super().__init__(name,age,exp,salary)
        self.level = level

    def print_data(self):
        print(self.level)

class Designers(Employee):

    def __init__(self,name,age,exp,salary,position):
        super().__init__(name,age,exp,salary)
        self.position = position
    def show(self):
        super().show()
        print(self.position)
objmain = Engineers("Manish",29,6,170000,"Senior")
objmain.print_data()
print(objmain.name)

objmain = Designers("Manish Reddy",29,6,170000,"Director")
objmain.show()
print(objmain.name)