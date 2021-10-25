#when to use class methrod when to use static methords ?



class Item:
    @staticmethod
    def is_inteter(num):
        '''


        This should do something that has a relationship with the class, but not something that must be unique per instance!

        '''


    @classmethod

    def instantiate_from_something(cls):
        '''
        This should also do something that has a relationship with the class, but usually, those are used to manipulate different
        structures of data to instantiate objects, like we have done with csv
        '''

item1 = Item()

item1.is_inteter(5)
item1.instantiate_from_something()