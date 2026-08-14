class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        from collections import Counter
        cnt = Counter()
        l = ans = 0
        for r, c in enumerate(s):
            cnt[c] += 1
            while cnt[c] > 2:
                cnt[s[l]] -= 1
                l += 1
            ans = max(ans, r - l + 1)
        return ans
        