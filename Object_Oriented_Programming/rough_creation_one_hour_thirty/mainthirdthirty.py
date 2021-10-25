import csv

class Item:
    pay_rate = 0.8 #The pay rate after 20% discount,Class level attribute

    all = []

    def __init__(self, name: str, price: float, quantitiy = 0):

        #run validation to the recieved arguments
        assert price >= 0, f"Prize {price} is not greater than or equal zero!"
        assert quantitiy >= 0, f"Quantity  {quantitiy} is not greater than or equal zero!"

        #Assign to self object
        self.name = name
        self.price = price         #instance atribute
        self.quantitiy = quantitiy
        #print(f"Inside constructor: {name}")
        # Actions to execute
        Item.all.append(self)

    def calculate_total_price(self):
        return self.price*self.quantitiy

    def apply_discount(self):
        self.price = self.price*self.pay_rate

    #creating a class methord
    @classmethod
    def instantiate_from_csv(cls):
        with open('items.csv', 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)

        for item in items:
            #print(item)
            Item(
                name=item.get('name'),
                price=float(item.get('price')),
                quantitiy=float(item.get('quantity'))
            )


    #We are creating a static methord
    #we never send an object as a first argument

    @staticmethod
    def is_integer(num):
        #we will count out the floats that are point zero
        #for i.e 5.0, 10.0
        if isinstance(num,float):
            #count out the floats that are point zero
            return num.is_integer()
        elif isinstance(num,int):
            return True
        else:
            return False



    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}',{self.price},{self.quantitiy})"





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



phone1 = Phone("jscPhonev10", 500,5,1)

print(phone1.calculate_total_price())


#phone2 = Phone("jscphonev20",700,5,1)

print(Item.all)
print(Phone.all)



'''print(Item.is_integer(7.0))


Item.instantiate_from_csv()
print(Item.all)

#print(Item.all)

for instance in Item.all:
    print(instance.name)
    
'''