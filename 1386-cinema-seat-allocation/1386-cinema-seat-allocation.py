class Solution:
    def maxNumberOfFamilies(self, n: int, reservedSeats: List[List[int]]) -> int:
        from collections import defaultdict
        rows = defaultdict(set)
        for r, s in reservedSeats:
            if 2 <= s <= 9:
                rows[r].add(s)

        ans = 2 * (n - len(rows))
        for taken in rows.values():
            left = not (taken & {2, 3, 4, 5})
            mid = not (taken & {4, 5, 6, 7})
            right = not (taken & {6, 7, 8, 9})
            ans += 2 if (left and right) else (1 if (left or mid or right) else 0)
        return ans
        