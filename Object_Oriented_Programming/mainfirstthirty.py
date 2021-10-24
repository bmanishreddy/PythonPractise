class Item:
    pay_rate = 0.8 #The pay rate after 20% discount,Class level attribute

    def __init__(self, name: str, price: float, quantitiy = 0):

        #run validation to the recieved arguments
        assert price >= 0, f"Prize {price} is not greater than or equal zero!"
        assert quantitiy >= 0, f"Quantity  {quantitiy} is not greater than or equal zero!"

        #Assign to self object
        self.name = name
        self.price = price         #instance atribute
        self.quantitiy = quantitiy
        #print(f"Inside constructor: {name}")

    def calculate_total_price(self):
        return self.price*self.quantitiy

    def apply_discount(self):
        self.price = self.price*self.pay_rate


item1 = Item("Phone",100,1)

print(item1.calculate_total_price())

item1.apply_discount()
print(item1.price)

item2 = Item("Laptop",1000,3)
item2.pay_rate = 0.7
item2.apply_discount()
print(item2.price)



#print(Item.__dict__) #All the atributes at class level
#print(item1.__dict__) #All the atribute for instance level

