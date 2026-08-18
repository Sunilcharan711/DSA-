class Solution:
    def largestInteger(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = -1
        for x in set(nums):
            cnt = sum(1 for i in range(n - k + 1) if x in nums[i:i + k])
            if cnt == 1:
                ans = max(ans, x)
        return ans