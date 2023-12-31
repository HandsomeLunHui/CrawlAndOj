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

# 冒泡排序
def bubble_sort(array:list)->list:
    for i in range(len(array)-1):
        for j in range(len(array)-1-i):
            if array[j] > array[j+1]:
                array[j],array[j+1]=array[j+1],array[j]
                print(array)

# 选择排序
def selection_sort(array:list)->list:
    for i in range(len(array)-1):
        # 记录最小值索引
        min_index=i
        for j in range(i+1,len(array)):
            if array[min_index]>array[j]:
                min_index=j
        array[i],array[min_index]=array[min_index],array[i]
        print(array)
    return array

# 数组与列表
# 1.数组元素类型要相同 2.数组长度固定

# 列表实现栈
class Stack:
    def __init__(self):
        self.stack=[]
    def push(self,value):
        self.stack.append(value)
    def pop(self):
        return self.stack.pop()
    def peek(self):
        if  self.stack:
            return self.stack[-1]
        else:
            return None
    def is_empty(self):
        return self.stack == []

# 括号匹配问题
def bracket_match(s:str)->bool:
    stack=Stack()
    for i in s:
        if i == "(":
            stack.push(")")
        elif i == "[":
            stack.push("]")
        elif i== "{":
            stack.push("}")
        elif stack.is_empty() or stack.peek() != i:
            return False
        else:
            stack.pop()
    return True

# 深度优先迷宫寻路问题
maze=[[]]

dirs=[
    lambda x,y: (x+1,y),
    lambda x,y: (x-1,y),
    lambda x,y: (x,y+1),
    lambda x,y: (x,y-1)
]

def maze_path(x1,y1,x2,y2):
    stack=[]
    stack.append((x1,y1))
    while stack:
        curNode=stack[-1]
        if curNode[0]==x2 and curNode[1]==y2:
            print("已经走到了终点")
            for i in stack:
                print(i)
            return True
        for dir in dirs:
            nextNode=dir(curNode[0],curNode[1])
            # 如果下一条路能走通
            if maze[nextNode[0][nextNode[1]]]==0:
                stack.append(nextNode)
                # 表示已经走过了
                maze[nextNode[0][nextNode[1]]]=2
                break
        else:
            maze[curNode[0][curNode[1]]]=2
            stack.pop()
    else:
        print("没有终点")
        return False

# python 链表
class Node:
    def __init__(self,item):
        self.item=item
        self.next=None

# 创建链表
def create_link_list(arr):
    head=Node(arr[0])
    for item in arr[1:]:
        node=Node(item)
        node.next=head
        head=node
    return head

# 尾插法
def create_link_list_tail(arr):
    head=Node(arr[0])
    tail=head
    for item in arr[1:]:
        node=Node(item)
        tail.next=node
        tail=node
    return head

# 实现linux文件目录
class Node:
    def __init__(self,name,type='dir'):
        self.name=name
        self.type=type
        self.child=[]
        self.parent=None

    def __repr__(self):
        return self.name

class FileSystemTree:
    def __init__(self):
        self.root=Node('/')
        self.now=self.root

    def mkdir(self,name):
        if name[-1]!='/':
            name+='/'
        node=Node(name)
        self.now.child.append(node)
        node.parent=self.now

    def ls(self):
        return self.now.child

    def cd(self,name):
        if name[-1]!='/':
            name+='/'
        if name=='../':
            self.now=self.now.parent
            return
        for child in self.now.child:
            if child.name==name:
                self.now=child
                return
        raise Exception("no such dir")

# 二叉树
class BiTreeNode:
    def __init__(self,data):
        self.data=data
        self.left=None
        self.right=None

# 二叉树的遍历
# 前序：中 左 右
# 中序：左 中 右
# 后序：左 右 中

def pre_order_traversal(root):
    if root:
        print(root.data)
        pre_order_traversal(root.left)
        pre_order_traversal(root.right)

def in_order_traversal(root):
    if root:
        in_order_traversal(root.left)
        print(root.data)
        in_order_traversal(root.right)

def post_order_traversal(root):
    if root:
        post_order_traversal(root.left)
        post_order_traversal(root.right)
        print(root.data)

# 二叉树的层序遍历
def level_order_traversal(root):
    from collections import deque
    queue=deque()
    if root:
        queue.append(root)
    while queue:
        node=queue.popleft()
        print(node.data)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


if __name__ == '__main__':
    # arry=[2,5,1,3,4,7,10,5,6]
    # print(arry)
    bracket="([{}])"
    print(bracket_match(bracket))