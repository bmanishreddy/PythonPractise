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





    def __repr__(self):
        return f"Item('{self.name}',{self.price},{self.quantitiy})"


Item.instantiate_from_csv()
print(Item.all)

#print(Item.all)
'''
for instance in Item.all:
    print(instance.name)
    
'''