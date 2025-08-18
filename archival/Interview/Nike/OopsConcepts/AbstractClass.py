from abc import ABC, abstractmethod

class AbstractDemo(ABC):

    def showprint(self,x):
        pass

    @abstractmethod
    def taskdemo(self):
        print("We are inside abract class")


class TestClass(AbstractDemo):

    def taskdemo(self):
        print("we are inside test class")
    def taskdemoTwo(self):
        print("we are inside test class")

objectDemo = TestClass()
objectDemo.taskdemoTwo()