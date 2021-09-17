def LargestSum(arr):
    if len(arr) == 0:
        return print("Null array")

    maxsum = currsum = arr[0]

    for n in arr[1:]:
        currsum = max(currsum+n,n)
        maxsum = max(currsum,maxsum)

    return maxsum


print(LargestSum([4,63,6-1,5,2,7,-44,4,3,6,77,99,-1,-67]))