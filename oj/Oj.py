#最短子数组
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

#螺旋矩阵
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return list()

    rows, columns = len(matrix), len(matrix[0])
    visited = [[False] * columns for _ in range(rows)]
    total = rows * columns
    order = [0] * total

    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    row, column = 0, 0
    directionIndex = 0
    for i in range(total):
        order[i] = matrix[row][column]
        visited[row][column] = True
        nextRow, nextColumn = row + directions[directionIndex][0], column + directions[directionIndex][1]
        if not (0 <= nextRow < rows and 0 <= nextColumn < columns and not visited[nextRow][nextColumn]):
            directionIndex = (directionIndex + 1) % 4
        row += directions[directionIndex][0]
        column += directions[directionIndex][1]
    return order

#反转字符串中的单词
# s="hello world"
# print(s.split())
# print(" ".join(s.split()[::-1]))

# 递归函数：调用自身与结束条件
def hanoi(n:int,a:str,b:str,c:str)->None:
    # 终止条件
    if n == 1:
        print(a,"->",c)
    else:
        hanoi(n-1,a,c,b)
        print(a,"->",c)
        hanoi(n-1,b,a,c)

# 顺序查找
def linear_search(array:list,target:int)->int:
    # for i in range(len(array)):
    #     if array[i] == target:
    #         return i
    # return -1
    for index,val in enumerate(array):
        if val == target:
            return index
    return -1

# 二分查找
def binary_search(array:list,target:int)->int:
    left=0
    right=len(array)-1
    while left <= right:
        middle=(left+right)//2
        if array[middle] == target:
            return middle
        elif array[middle] < target:
            left=middle+1
        else:
            right=middle-1
    return -1

if __name__ == '__main__':
    hanoi(3,"A","B","C")