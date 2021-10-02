class Employee:

    #Class level atribute
    employeeLocation = "Dallas, Texas"

    #we are defining a parameterized constructor
    def __init__(self,name,salary,experience,age):
        #initate the atributes
        self.name = name
        self.age = age
        self.salary = salary
        self.experience = experience


#Create an object for the atribute for the class employee

emplyeeObject = Employee("Manish",50000,6,30)

print("The name of the employee = ",emplyeeObject.name)
print("Location of the employee =", Employee.employeeLocation)
print("Employee salary =",emplyeeObject.salary)

