class Solution:
    def lexicographicallySmallestArray(self, nums: List[int], limit: int) -> List[int]:
        n = len(nums)
        idx = sorted(range(n), key=lambda i: nums[i])
        res = [0] * n
        i = 0
        while i < n:
            j = i + 1
            while j < n and nums[idx[j]] - nums[idx[j - 1]] <= limit:
                j += 1
            group = sorted(idx[i:j])          # positions in this group
            for pos, k in zip(group, range(i, j)):
                res[pos] = nums[idx[k]]        # values already ascending
            i = j
        return res