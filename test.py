import numpy as np
import os
from mylib import type, operator, reader, writer

# files = os.listdir('.\\input')
# for file in files:

file = ['1_1.txt', '2_1.txt', '3_1.txt', '4_1.txt'][0]

# 读取文件
data = reader.readFile('.\\input\\' + file)

# 计算单元刚度矩阵
for unit in data.units:
    unit.Ke = operator.calculateKe(unit)

# 计算总刚
middata = type.MidData(data)
n = len(data.points)*2
middata.K = np.zeros((n, n))
for unit in data.units:
    operator.integrateKe(unit, middata.K)

# 计算等效荷载向量
middata.P = np.zeros((n,))
operator.integratePe(data.payloads, middata.P)

# 引入位移边界条件和解方程
operator.integrateX(data.constraints, middata.K, middata.P)
operator.calculateA(middata)

# 写入文件
output = operator.gennerate(middata)

save_dir = f".\\result"
os.makedirs(save_dir, exist_ok=True)

writer.writeFile(f"{save_dir}\\{file.split('.')[0]}.txt", output)
print("finished.")
