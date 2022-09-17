
class loveUtils:
    def findMedian(nums):
        nums.sort()
        mid = len(nums) // 2
        res = (nums[mid] + nums[~mid]) / 2
        return res