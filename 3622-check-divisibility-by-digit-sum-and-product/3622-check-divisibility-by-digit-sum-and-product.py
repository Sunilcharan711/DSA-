class Solution:
    def checkDivisibility(self, n: int) -> bool:
        s, p = 0, 1
        for ch in str(n):
            d = int(ch)
            s += d
            p *= d
        return n % (s + p) == 0
        