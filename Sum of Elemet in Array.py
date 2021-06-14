
nums = [1, 2, 3, 4, 5]
output = [nums[0]]
for i in range (1, len(nums)):
        nums[i] += nums[i - 1]
        output.append(nums[i])
print(output[:])
