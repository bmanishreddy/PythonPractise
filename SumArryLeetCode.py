class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dictarr = {}
        for i in range(len(nums)):
            
            n = target - nums[i]
            if n in dictarr:
                return[i,dictarr[n]]
            dictarr[nums[i]] = i
                
        
