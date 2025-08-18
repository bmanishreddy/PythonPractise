class ParentEle:
    def __init__(self):

        #Protected member
       #_ has the value to protect
        self._mobilenumber = 3006660000


class ChildEle(ParentEle):
    def __init__(self):
        ParentEle.__init__(self)
        print(self._mobilenumber)



objtemp = ChildEle()
print(objtemp._mobilenumber)

