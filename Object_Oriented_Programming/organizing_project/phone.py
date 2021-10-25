from item import Item

class Phone(Item):
    #all =[]
    def __init__(self, name: str, price: float, quantitiy=0, broken_phones=0):

        #call to super function to have acces to all artibutes and methords
        super().__init__(name, price, quantitiy)

        #run validation to the recieved arguments


        assert broken_phones >=0, f"Boken phones {broken_phones} is not grater than or equal to zero!"


        self.broken_phones = broken_phones
        #print(f"Inside constructor: {name}")
        # Actions to execute
       # Phone.all.append(self)
