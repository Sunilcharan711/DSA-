class Solution:
    def smallestPalindrome(self, s: str, k: int) -> str:
        from collections import Counter
        from math import comb
        
        cnt = Counter(s)
        mid = ""
        half = [0] * 26
        for i in range(26):
            c = chr(97 + i)
            if cnt[c] & 1:
                mid = c
            half[i] = cnt[c] // 2
        
        n = sum(half)
        if n == 0:
            return s if k == 1 else ""
        
        LIMIT = k
        
        def count(h):
            # number of distinct permutations of multiset h, capped at LIMIT
            total = sum(h)
            res = 1
            rem = total
            for x in h:
                if x:
                    res *= comb(rem, x)
                    rem -= x
                    if res >= LIMIT:
                        return LIMIT
            return res
        
        if count(half) < k:
            return ""
        
        res = []
        for _ in range(n):
            for i in range(26):
                if half[i]:
                    half[i] -= 1
                    c = count(half)
                    if c >= k:
                        res.append(chr(97 + i))
                        break
                    k -= c
                    half[i] += 1
        
        first = "".join(res)
        return first + mid + first[::-1]