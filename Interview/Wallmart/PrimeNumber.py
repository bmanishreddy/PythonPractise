from math import sqrt

print(9%3)
def prime_number(number):
        if number == 1:
            return -1
        for i in range(2, number):
            if (number % i) == 0:
                return i
                break
            i += 1
        if(number == number):
            return -1
        else:
            return i





print(prime_number(18))