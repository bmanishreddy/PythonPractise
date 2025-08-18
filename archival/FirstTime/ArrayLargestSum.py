def larget(arr):
    if len(arr) == 0:
        return print("Too small ")

    max_sum = current_sum = arr[0]


    for num in arr[1:]:
        current_sum = max(current_sum+num, num)
        max_sum = max(current_sum,max_sum)

    return max_sum

print(larget([7,1,3,4,6,-1,3,5,7,4,-10,-19]))