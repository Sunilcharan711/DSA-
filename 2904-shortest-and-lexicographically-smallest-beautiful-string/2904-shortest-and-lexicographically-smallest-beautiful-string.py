class Solution:
    def shortestBeautifulSubstring(self, s: str, k: int) -> str:
        n = len(s)
        left = 0
        ones = 0
        ans = ""

        for right in range(n):
            if s[right] == '1':
                ones += 1

            while ones > k:
                if s[left] == '1':
                    ones -= 1
                left += 1

            if ones == k:
                # Remove leading zeros to get the shortest substring
                while s[left] == '0':
                    left += 1

                curr = s[left:right + 1]

                if ans == "" or len(curr) < len(ans) or \
                   (len(curr) == len(ans) and curr < ans):
                    ans = curr

        return ans
        