# -*- coding: utf-8 -*-

# 魔术方法
class Student(object):
    def __init__(self, student_list):
        self.student = student_list
        self.age=18

    # 魔术方法
    def __getitem__(self, item):
        return self.student[item]

    def __str__(self):
        # 格式化输出
        return ','.join(self.student)

    # 类长度
    def __len__(self):
        return len(self.student)

    # 绝对值
    def __abs__(self):
        return abs(self.age)

# 向量运算
class myVector:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __add__(self, other):
        return myVector(self.x+other.x,self.y+other.y)

    def __sub__(self, other):
        return myVector(self.x-other.x,self.y-other.y)

    def __mul__(self, other):
        return myVector(self.x*other.x,self.y*other.y)

    def __str__(self):
        return '(x:%d,y:%d)'%(self.x,self.y)

# 多态
class Animal:
    def say(self):
        print('励志')

class Dog(Animal):
    def say(self):
        print('汗汗汗')

class Cat(Animal):
    def say(self):
        print('喋喋喋')

def animal_test():
    animal=Animal()
    animal.say()

    animal=Dog()
    animal.say()

    animal=Cat()
    animal.say()

# 鸭子类型
class Duck:
    def say(self):
        print('嘎嘎嘎')

class Dog:
    def say(self):
        print('汗汗汗')

def duck_test():
    animal=Duck
    animal().say()

    animal=Dog
    animal().say()

# 抽象基类 导入python的全局基类
from abc import ABCMeta, abstractmethod

# 限制使用者必须按照某种规则
class Animal(metaclass=ABCMeta):
    @abstractmethod
    def say(self):
        pass
    @abstractmethod
    def run(self):
        pass

class Bird(Animal):
    def say(self):
        print('汗汗汗')

    def run(self):
        print('fly')

# 类变量与实例变量
class A:
    # 类变量
    a=1
    def __init__(self,x,y):
        # 实例变量
        self.x=x
        self.y=y

# 类方法 静态方法与实例方法
# 实例方法只能通过实例化对象调用
# 静态方法调用 类.类方法

class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day

    def __str__(self):
        return '%d-%d-%d'%(self.year,self.month,self.day)

    # 静态方法
    # 调用:Date.is_date_valid('2018-12-12')
    # Date:类本身 date=Date() 类实例对象
    @staticmethod
    def is_date_valid(date_str):
        year,month,day=map(int,date_str.split('-'))
        # 静态方法返回类的时候是写上当前类名
        return Date(year,month,day)

    # 类方法 传入一个cls参数
    @classmethod
    def from_string(cls,date_str):
        year,month,day=map(int,date_str.split('-'))
        # cls 指向这个类
        return cls(year,month,day)

# 私有属性与数据封装
class B:
    def __init__(self,b):
        # 私有属性 相当于c++中的private成员变量 双下划线__
        self.__b=b

# try except finally
# 在异常捕获中如果有 return语句 且finally中有return语句 则会返回finally中的return
def tryExceptFinally():
    try:
        a = 10 / 0
        raise KeyError
    except Exception as e:
        print(e)
    else:
        # 没有异常才会执行 else 里面的语句
        print('成功')
    finally:
        # 有没有异常都会执行
        print('结束')

# 上下文管理器协议
class Sample():
    def __enter__(self):
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')

    def do_something(self):
        print('do something')



def contextlib_test():
    import contextlib

    @contextlib.contextmanager
    # 此装饰器可以将一个函数变成一个上下文管理器
    def file_open(file_name):
        print('file open')
        yield {}
        print('file close')

    with file_open('file') as f:
        print("file processing")

# append 和 extend的区别
def append_extend_test():
    a=[1,2,3]
    b=[4,5,6]
    # append 是更改为一个对象后插入
    a.append(b)
    print(a)
    # extend 是迭代插入
    a.extend(b)
    print(a)

# 维护已经排序的序列

def heapq_test():
    import bisect

    inter_list=[1,2,3,6]
    bisect.insort(inter_list,7)
    bisect.insort(inter_list,2)
    bisect.insort(inter_list,5)
    bisect.insort(inter_list,1)
    bisect.insort(inter_list,6)
    print(inter_list)

# 列表推导式
def list_comprehension_test():
    b=[i for i in range(10) if i%2==0]
    print(b)
    # 字典推导式
    c={i:i for i in range(10)}
    print(c)

# getattr getattribute魔法函数
def getattr_test():
    class A:
        def __init__(self):
            self.a=1
            self.b=2

        def __getattr__(self, item):
            # 查找不到属性值时会进入该魔法函数
            return 'no attribute'

        def __getattribute__(self, item):
            # 访问函数无条件进入该函数
            return 'no attribute'




if __name__ == '__main__':
    a=[1,2,3,6]
    b=a.copy()
    b.append(10)
    print(a)