def array_pairsum(array,k):
    if len(array)<2:
        return print("Array size is less than two")

    seen = set()
    output = set()

    for num in array:
        target = k - num
        if target not in seen:
            seen.add(num)

        else:
            output.add((min(num,target),max(num,target)))
    print(output)

array_pairsum([1,2,3,4,2,0],4)


