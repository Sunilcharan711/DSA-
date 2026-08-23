class Solution:
    def sumGame(self, num: str) -> bool:
        n = len(num)
        half = n // 2
        
        sum_l = sum_r = q_l = q_r = 0
        for i, c in enumerate(num):
            if i < half:
                if c == '?': q_l += 1
                else: sum_l += int(c)
            else:
                if c == '?': q_r += 1
                else: sum_r += int(c)
        
        k = q_r - q_l          # surplus '?' on the right
        if k % 2:              # odd total '?' → Alice wins
            return True
        return sum_l - sum_r != 9 * (k // 2)
        