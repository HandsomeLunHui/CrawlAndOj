def minSubArrayLength(target:int,array:list):
    start = 0
    end = 0
    min_length = float('inf')
    total = 0
    while end < len(array):
        total += array[end]
        while total >= target:
            min_length = min(min_length,end-start+1)
            total -= array[start]
            start += 1
        end += 1
    return min_length if min_length != float('inf') else 0