from typing import List

def Sort(nums: List[int]) -> List[int]:
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if nums[i] > nums[j]:
                temp = nums[i]
                nums[i] = nums[j]
                nums[j] = temp

    return nums


def Search(nums: List[int], key: int) -> bool:
    for nums in nums:
        if num == key:
            return True

    return False
            