class Solution:
    def missingInteger(self, nums: List[int]) -> int:
        n = len(nums)
        i = 1
        while i < n and nums[i] == nums[i-1] + 1:
            i += 1
        s = sum(nums[:i])
        st = set(nums)
        while s in st:
            s += 1
        return s
        