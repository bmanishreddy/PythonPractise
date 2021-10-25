from item import Item
from phone import Phone
from keyboard import Keyboard

'''
Item.instantiate_from_csv()

print(Item.all)

'''

item1 = Item("MyItem",750,6)


print(item1.name)

item1.name = "OtherItem"

print(item1.name)


#Concept of encapsulation
item1.apply_increment(0.2)

print(item1.price)


item1 = Item("MyItem",750,6)




#Abstraction... only method that is important is accisable
item1.send_email()



#Polymorphysm

phone1 = Phone("MyItem",1000,3)

phone1.apply_discount()
print(phone1.price)

item1 = Keyboard("maniKeyboard",1000,3)
item1.apply_discount()
print(item1.price)