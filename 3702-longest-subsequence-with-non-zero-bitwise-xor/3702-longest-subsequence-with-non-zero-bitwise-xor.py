class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        total = 0
        for x in nums:
            total ^= x
        if total != 0:
            return len(nums)
        return len(nums) - 1 if any(nums) else 0
        
        