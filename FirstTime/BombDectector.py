#Input: nums = [2,7,11,15], target = 9
#3Output: [0,1]
nums = [2, 7, 11, 15]
target = 9

def sumnum(nums,target):
    hashmap = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in hashmap:
            return [i, hashmap[complement]]
        hashmap[nums[i]] = i




print(sumnum(nums,target))