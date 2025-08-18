def nextSquare():
    i = 1

    # An Infinite loop to generate squares
    while True:
        yield i * i

        i += 1

print(nextSquare().__next__())
print(nextSquare().__next__())
print(nextSquare().__next__())
print(nextSquare().__next__())
print(nextSquare().__init__())