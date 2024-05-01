# 导入所需的库
import os
import re
import datetime
from datetime import datetime
import chardet
import openpyxl
import pandas as pd

# 获取脚本所在文件夹目录下所有文件的读写权限
for file in os.listdir():
    os.chmod(os.path.join(os.getcwd(), file), 0o777)

#新建一个 tmp.txt 文本储存临时数据
# 检查文件是否存在
if not os.path.exists('tmp.txt'):
    # 如果不存在，创建一个新文件
    with open('tmp.txt', 'w') as f:
        pass
else:
    # 如果存在，清空文件内容
    with open('tmp.txt', 'w') as f:
        f.truncate(0)

# 获取该文件夹中 cssj.txt 文件的内容，存储到 tmp.txt 文件中
# 使用chardet库检测cssj.txt文件的编码格式
with open("cssj.txt", "rb") as f:
    data = f.read()
    encoding = chardet.detect(data)["encoding"]
# 使用检测到的编码格式打开cssj.txt文件，并以UTF-8编码写入tmp.txt文件
with open("cssj.txt", "r", encoding=encoding) as f1, open("tmp.txt", "w", encoding="utf-8") as f2:
    f2.write(f1.read())

# 读取 tmp.txt 文件，检测到像 多个（最少两个、最多四个）汉字 加 西文逗号 加 多个阿拉伯数字 加 小数点 加 阿拉伯数字 加汉字“分” 的字符串，就保留。
# 删除所有不满足条件的字符
with open("tmp.txt", "r+", encoding="utf-8") as f:
    content = f.read()
    # 定义正则表达式匹配所需的字符串
    pattern = re.compile(r"\w{2,4},\d+\.\d+分")
    # 找出所有匹配的字符串，并用换行符连接起来
    result = "\n".join(pattern.findall(content))
    # 清空文件并写入结果
    f.seek(0)
    f.truncate()
    f.write(result)

# 创建result文件夹
if not os.path.exists('result'):
    os.makedirs('result')

# 创建Excel文件名
filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
filepath = os.path.join('result', filename)

# 读取tmp.txt文件内容
with open('tmp.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 处理数据并保存到DataFrame
data = []
for line in lines:
    name, score = line.strip().split(',')
    score = float(score.rstrip('分'))
    data.append([name, score])

df = pd.DataFrame(data, columns=['姓名', '成绩'])

# 对成绩进行排序
df.sort_values(by='成绩', ascending=False, inplace=True)

# 添加名次列，同分的人占用同一个名次
df['名次'] = df['成绩'].rank(method='min', ascending=False)

# 将名次列移动到第一列
df = df[['名次', '姓名', '成绩']]

# 保存到Excel文件
df.to_excel(filepath, index=False)

#删除tmp文件
# 检查tmp.txt文件是否存在
if os.path.exists('tmp.txt'):
    # 如果存在，删除文件
    os.remove('tmp.txt')

# 清空cssj.txt文件内容
with open('cssj.txt', 'w') as f:
    f.truncate(0)

#完成输出
print("✅ 请前往result文件夹中查看成绩单")