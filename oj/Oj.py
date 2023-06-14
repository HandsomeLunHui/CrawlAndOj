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
