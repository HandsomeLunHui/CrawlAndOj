import execjs
import json

item={
    'name': '凯文-杜兰特',
    'image': 'durant.png',
    'birthday': '1988-09-29',
    'height': '208cm',
    'weight': '108.9KG'
}

# 文件路径
file='crypto.js'
# 获取js执行环境
node=execjs.get()
# 将js代码放入执行环境中 相当于已经编译
ctx=node.compile(open(file).read())


js=f"getToken('{json.dumps(item,ensure_ascii=False)}')"
print(js)
# 调用js代码中的某些函数 ctx.eval(js)
result=ctx.eval(js)
print(result)