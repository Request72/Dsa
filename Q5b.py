def longest_hike(nums, k):
    if not nums:
        return 0

    left = right = 0
    max_length = 1
    current_gain = 0

    while right < len(nums) - 1:
        right += 1


        if nums[right] > nums[right-1]:
            current_gain += nums[right] - nums[right-1]


        while current_gain > k and left < right:
            if nums[left+1] > nums[left]:
                current_gain -= nums[left+1] - nums[left]
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length

trail = [4, 2, 1, 4, 3, 4, 5, 8, 15]
k = 3
result = longest_hike(trail, k)
print(f"Longest hike: {result}")