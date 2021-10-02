
class PolyDemo:

    def __init__(self,twosum,threesum):
        #self.x = x
        #self.y = y
        #self.z = z
        self.twosum = twosum
        self.threesum = threesum



    def add(self,x,y,z=0):
        return (self.threesum,x+y+z)

objPoly = PolyDemo("The value of two sum","The value of three sum")
print(objPoly.add(4,8))
