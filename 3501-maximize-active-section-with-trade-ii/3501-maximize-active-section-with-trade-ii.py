from bisect import bisect_left, bisect_right


class Solution:
    def maxActiveSectionsAfterTrade(self, s, queries):
        n = len(s)
        total_ones = s.count("1")

        # Run-length encoding: (start, end, bit)
        runs = []
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            runs.append((i, j - 1, s[i]))
            i = j

        zero_runs = [(left, right) for left, right, bit in runs if bit == "0"]

        # Each candidate is a 1-run surrounded by 0-runs:
        # (one_l, one_r, one_length,
        #  left_zero_l, left_zero_r,
        #  right_zero_l, right_zero_r,
        #  full_merged_gain)
        candidates = []

        for i in range(1, len(runs) - 1):
            one_l, one_r, bit = runs[i]

            if bit != "1":
                continue

            if runs[i - 1][2] != "0" or runs[i + 1][2] != "0":
                continue

            left_zero_l, left_zero_r, _ = runs[i - 1]
            right_zero_l, right_zero_r, _ = runs[i + 1]

            one_length = one_r - one_l + 1

            # The removed one-block is included again in the activated merged
            # block, so net gain equals the lengths of both adjacent zero-runs.
            full_merged_gain = (
                left_zero_r - left_zero_l + 1
                + right_zero_r - right_zero_l + 1
            )

            candidates.append((
                one_l,
                one_r,
                one_length,
                left_zero_l,
                left_zero_r,
                right_zero_l,
                right_zero_r,
                full_merged_gain
            ))

        def build_tree(values, identity, operation):
            size = 1
            while size < len(values):
                size <<= 1

            tree = [identity] * (2 * size)

            for index, value in enumerate(values):
                tree[size + index] = value

            for index in range(size - 1, 0, -1):
                tree[index] = operation(tree[index * 2], tree[index * 2 + 1])

            return tree, size

        def query_tree(tree, size, left, right, identity, operation):
            if left > right:
                return identity

            left += size
            right += size
            result = identity

            while left <= right:
                if left & 1:
                    result = operation(result, tree[left])
                    left += 1

                if not (right & 1):
                    result = operation(result, tree[right])
                    right -= 1

                left //= 2
                right //= 2

            return result

        zero_lengths = [right - left + 1 for left, right in zero_runs]
        zero_starts = [left for left, right in zero_runs]
        zero_ends = [right for left, right in zero_runs]

        candidate_starts = [item[0] for item in candidates]
        candidate_ends = [item[1] for item in candidates]
        candidate_one_lengths = [item[2] for item in candidates]
        candidate_full_gains = [item[7] for item in candidates]

        zero_tree, zero_tree_size = build_tree(zero_lengths, 0, max)

        min_one_tree, min_one_tree_size = build_tree(
            candidate_one_lengths,
            float("inf"),
            min
        )

        gain_tree, gain_tree_size = build_tree(
            candidate_full_gains,
            0,
            max
        )

        answer = []

        for query_left, query_right in queries:
            # A removable 1-run must be strictly inside [query_left, query_right].
            first_candidate = bisect_right(candidate_starts, query_left)
            last_candidate_exclusive = bisect_left(candidate_ends, query_right)

            # No valid first step means no valid trade.
            if first_candidate >= last_candidate_exclusive:
                answer.append(total_ones)
                continue

            # Largest zero-run that intersects the query.
            first_zero = bisect_left(zero_ends, query_left)
            last_zero = bisect_right(zero_starts, query_right) - 1

            max_zero_length = 0

            if first_zero <= last_zero:
                if first_zero == last_zero:
                    max_zero_length = (
                        min(query_right, zero_runs[first_zero][1])
                        - max(query_left, zero_runs[first_zero][0])
                        + 1
                    )
                else:
                    left_partial = (
                        zero_runs[first_zero][1]
                        - max(query_left, zero_runs[first_zero][0])
                        + 1
                    )

                    right_partial = (
                        min(query_right, zero_runs[last_zero][1])
                        - zero_runs[last_zero][0]
                        + 1
                    )

                    max_zero_length = max(left_partial, right_partial)

                    max_zero_length = max(
                        max_zero_length,
                        query_tree(
                            zero_tree,
                            zero_tree_size,
                            first_zero + 1,
                            last_zero - 1,
                            0,
                            max
                        )
                    )

            # Choice 1:
            # Remove a one-run, then activate a separate zero-run.
            shortest_one_length = query_tree(
                min_one_tree,
                min_one_tree_size,
                first_candidate,
                last_candidate_exclusive - 1,
                float("inf"),
                min
            )

            separate_gain = max_zero_length - shortest_one_length

            # Choice 2:
            # Activate the merged zero-run around the removed one-run.
            def clipped_merged_gain(candidate_index):
                (
                    one_l,
                    one_r,
                    one_length,
                    left_zero_l,
                    left_zero_r,
                    right_zero_l,
                    right_zero_r,
                    full_gain
                ) = candidates[candidate_index]

                left_zero_count = (
                    left_zero_r - max(query_left, left_zero_l) + 1
                )

                right_zero_count = (
                    min(query_right, right_zero_r) - right_zero_l + 1
                )

                return left_zero_count + right_zero_count

            best_merged_gain = clipped_merged_gain(first_candidate)

            if first_candidate != last_candidate_exclusive - 1:
                best_merged_gain = max(
                    best_merged_gain,
                    clipped_merged_gain(last_candidate_exclusive - 1)
                )

            # Candidates in the middle are fully inside the query.
            best_merged_gain = max(
                best_merged_gain,
                query_tree(
                    gain_tree,
                    gain_tree_size,
                    first_candidate + 1,
                    last_candidate_exclusive - 2,
                    0,
                    max
                )
            )

            best_gain = max(0, separate_gain, best_merged_gain)
            answer.append(total_ones + best_gain)

        return answer