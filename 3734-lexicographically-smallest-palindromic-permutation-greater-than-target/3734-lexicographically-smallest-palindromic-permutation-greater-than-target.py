from collections import Counter

class Solution:
    def lexPalindromicPermutation(self, s: str, target: str) -> str:
        n = len(s)
        c = Counter(s)

        if sum(v % 2 for v in c.values()) > 1:
            return ""

        mid = next((x for x in c if c[x] % 2), "")
        h = []
        for x in sorted(c):
            h += [x] * (c[x] // 2)

        m = n // 2
        t = target[:m]
        cnt = Counter(h)

        ok = True
        for x in t:
            if cnt[x] == 0:
                ok = False
                break
            cnt[x] -= 1

        def make(x):
            return x + mid + x[::-1] if n % 2 else x + x[::-1]

        if ok and make(t) > target:
            return make(t)

        used = Counter()
        for i in range(m):
            used[t[i]] += 1
            if used[t[i]] > Counter(h)[t[i]]:
                break
        else:
            i = m

        for j in range(i, -1, -1):
            rem = Counter(h)
            for x in t[:j]:
                rem[x] -= 1

            if any(v < 0 for v in rem.values()):
                continue

            for ch in map(chr, range(ord(t[j]) + 1, ord('z') + 1)) if j < m else []:
                if rem[ch]:
                    rem[ch] -= 1
                    left = t[:j] + ch
                    for x in sorted(rem):
                        left += x * rem[x]
                    return make(left)

        return ""
        