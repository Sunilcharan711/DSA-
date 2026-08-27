class Solution:
    def lexGreaterPermutation(self, s: str, target: str) -> str:
        n = len(s)

        # Count characters in s
        total = [0] * 26
        for ch in s:
            total[ord(ch) - ord('a')] += 1

        # Try changing target at position i.
        # We go from right to left because we want the
        # lexicographically smallest possible answer.
        for i in range(n - 1, -1, -1):

            # Characters remaining after using target[:i]
            cnt = total[:]

            possible = True

            for j in range(i):
                x = ord(target[j]) - ord('a')
                cnt[x] -= 1

                if cnt[x] < 0:
                    possible = False
                    break

            if not possible:
                continue

            # Find the smallest character greater than target[i]
            cur = ord(target[i]) - ord('a')

            for c in range(cur + 1, 26):
                if cnt[c] > 0:
                    # Use this larger character
                    cnt[c] -= 1

                    # Put remaining characters in sorted order
                    suffix = []
                    for x in range(26):
                        suffix.extend([chr(x + ord('a'))] * cnt[x])

                    return target[:i] + chr(c + ord('a')) + ''.join(suffix)

        return ""