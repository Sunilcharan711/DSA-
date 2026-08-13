class Solution:
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        n = len(s)
        arr = list(s)

        size = 4 * n
        ch_l = [''] * size
        ch_r = [''] * size
        length = [0] * size
        pref = [0] * size
        suf = [0] * size
        best = [0] * size

        def pull(node, l, r, mid):
            L, R = 2 * node, 2 * node + 1
            length[node] = r - l + 1
            ch_l[node] = ch_l[L]
            ch_r[node] = ch_r[R]

            pref[node] = pref[L]
            if pref[L] == (mid - l + 1) and ch_r[L] == ch_l[R]:
                pref[node] += pref[R]

            suf[node] = suf[R]
            if suf[R] == (r - mid) and ch_r[L] == ch_l[R]:
                suf[node] += suf[L]

            best[node] = max(best[L], best[R])
            if ch_r[L] == ch_l[R]:
                best[node] = max(best[node], suf[L] + pref[R])

        def build(node, l, r):
            if l == r:
                ch_l[node] = ch_r[node] = arr[l]
                length[node] = pref[node] = suf[node] = best[node] = 1
                return
            mid = (l + r) // 2
            build(2 * node, l, mid)
            build(2 * node + 1, mid + 1, r)
            pull(node, l, r, mid)

        def update(node, l, r, idx, c):
            if l == r:
                ch_l[node] = ch_r[node] = c
                return
            mid = (l + r) // 2
            if idx <= mid:
                update(2 * node, l, mid, idx, c)
            else:
                update(2 * node + 1, mid + 1, r, idx, c)
            pull(node, l, r, mid)

        build(1, 0, n - 1)

        res = []
        for c, idx in zip(queryCharacters, queryIndices):
            update(1, 0, n - 1, idx, c)
            res.append(best[1])

        return res
        
        