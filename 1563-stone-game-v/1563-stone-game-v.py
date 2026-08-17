class Solution:
    def stoneGameV(self, stoneValue: List[int]) -> int:
        n = len(stoneValue)
        if n == 1:
            return 0

        pre = [0] * (n + 1)
        for i, v in enumerate(stoneValue):
            pre[i + 1] = pre[i] + v

        dp = [[0] * n for _ in range(n)]
        # maxL[i][j] = max over t in [i,j] of ( sum(i,t) + dp[i][t] )
        # maxR[i][j] = max over t in [i,j] of ( sum(t,j) + dp[t][j] )
        maxL = [[0] * n for _ in range(n)]
        maxR = [[0] * n for _ in range(n)]
        for i in range(n):
            maxL[i][i] = maxR[i][i] = stoneValue[i]

        mid = list(range(n))  # monotone split pointer per i

        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                total = pre[j + 1] - pre[i]

                k = mid[i]
                while (pre[k + 1] - pre[i]) * 2 < total:
                    k += 1
                mid[i] = k

                best = 0
                # splits t < k: left sum < right sum -> keep left
                if k > i:
                    best = maxL[i][k - 1]
                # split t == k
                if k <= j - 1:
                    left = pre[k + 1] - pre[i]
                    right = total - left
                    if left * 2 == total:
                        cand = max(left + dp[i][k], right + dp[k + 1][j])
                    else:
                        cand = right + dp[k + 1][j]
                    if cand > best:
                        best = cand
                # splits t > k: left sum > right sum -> keep right
                if k + 2 <= j:
                    if maxR[k + 2][j] > best:
                        best = maxR[k + 2][j]

                dp[i][j] = best
                maxL[i][j] = max(maxL[i][j - 1], total + best)
                maxR[i][j] = max(maxR[i + 1][j], total + best)

        return dp[0][n - 1]
        