import csv

class Item:
    pay_rate = 0.8 #The pay rate after 20% discount,Class level attribute

    all = []

    def __init__(self, name: str, price: float, quantitiy = 0):

        #run validation to the recieved arguments
        assert price >= 0, f"Prize {price} is not greater than or equal zero!"
        assert quantitiy >= 0, f"Quantity  {quantitiy} is not greater than or equal zero!"

        #Assign to self object
        self.__name = name          #We are creating a private variable
        self.__price = price         #instance atribute
        self.quantitiy = quantitiy
        #print(f"Inside constructor: {name}")
        # Actions to execute
        Item.all.append(self)

    @property
    def price(self):

        return self.__price

    def apply_discount(self):
        self.__price = self.__price * self.pay_rate

    def apply_increment(self, increment_value):
        self.__price = self.__price + self.__price * float(increment_value)

    @property
    #propertly read-only attribute
    def name(self):
        print("you are trying to get name")
        return self.__name

    #set a new valuefor the name attribute
    @name.setter
    def name(self,value):

        if len(value) > 10:
            raise Exception("The name is too long!!")
        else:
            self.__name = value




    def calculate_total_price(self):
        return self.__price * self.quantitiy



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
        return f"{self.__class__.__name__}('{self.name}',{self.__price},{self.quantitiy})"


    def __connect(self,smpt_server):
        pass
    def __prepare_body(self):
        return f"""
        have {self.name}{self.quantitiy} detials
        """
    def __send(self):
        pass

    def send_email(self):
        self.__connect("")
        self.__prepare_body()
        self.__send()



'''
    #read only atribure and cannot be over ridden
    @property
    def read_only_name(self):
        return "AAA"

'''
