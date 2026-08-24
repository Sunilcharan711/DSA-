class Solution:
    def stoneGameVIII(self, stones: List[int]) -> int:
        n = len(stones)
        prefix = list(accumulate(stones))
        
        # dp represents the best score difference (current player - opponent)
        # achievable if the game were to start with taking the prefix at index i (>= i)
        dp = prefix[-1]
        for i in range(n - 2, 0, -1):
            dp = max(dp, prefix[i] - dp)
        
        return dp
        