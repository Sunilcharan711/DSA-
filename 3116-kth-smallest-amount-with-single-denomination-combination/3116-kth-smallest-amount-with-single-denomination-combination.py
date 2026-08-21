class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        from math import lcm

        # Drop coins that are multiples of another coin — they add nothing.
        coins.sort()
        base = []
        for c in coins:
            if not any(c % b == 0 for b in base):
                base.append(c)

        hi = k * base[0]          # k-th multiple of the smallest coin is an upper bound
        m = len(base)

        # Inclusion–exclusion terms: (lcm of subset, sign), pruned when lcm > hi
        terms = []
        def dfs(i, cur, cnt):
            if i == m:
                if cnt:
                    terms.append((cur, 1 if cnt & 1 else -1))
                return
            dfs(i + 1, cur, cnt)                      # skip base[i]
            nl = base[i] if cur == 0 else lcm(cur, base[i])
            if nl <= hi:                              # else every multiple is out of range
                dfs(i + 1, nl, cnt + 1)
        dfs(0, 0, 0)

        def count(x):
            return sum(sign * (x // l) for l, sign in terms)

        lo = 1
        while lo < hi:
            mid = (lo + hi) // 2
            if count(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
        