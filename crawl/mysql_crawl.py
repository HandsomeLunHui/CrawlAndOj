import pymysql


class DBHelper:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="217217",
            database="spiders",
            charset="utf8",
        )
        self.cur = self.conn.cursor()

    # 执行不需要数据返回的语句 插入更新删除操作需要调用commit
    def  execute(self, sql, params=None):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
            print("successiful")
        except Exception as e:
            print(e)
            self.conn.rollback()

    # 执行需要返回数据的语句
    def  query(self, sql, params=None):
        self.cur.execute(sql, params)
        result = self.cur.fetchall()
        return result

    def __del__(self):
        self.cur.close()
        self.conn.close()

# db=pymysql.connect(host="localhost",user="root",password="217217",charset="utf8")
# cursor=db.cursor()
# cursor.execute("select version()")
# data=cursor.fetchone()
# # cursor.execute("create database spiders default character set utf8mb4")
# print(data)

# 字典构造
# data={
#     "id":"201901937",
#     "name":"小明",
#     "age":18
# }
#
# keys=",".join(data.keys())
# values=",".join(['%s']*len(data))
# print(keys,values)

if __name__ == '__main__':
    db=DBHelper()
    user="Robert');DROP TABLE students;--"
    id="201901932"
    age=18
    sql="insert into students (id,age,name) values (%s,%s,%s)"
    params=(id,age,user)
    db.execute(sql,params)
    pass
