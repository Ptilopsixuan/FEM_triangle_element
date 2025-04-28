import numpy as np
import os
from mylib import type, operator, reader, writer, create

l = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.2, 5.6, 6.0, 6.4, 6.8, 7.2, 7.6, 8.0]
n_l = []
for i in range(len(l)):
    n_l.append(int(l[i] / 0.1) + 1)
h = 4
n_h = 40 + 1
force = 1e7

# name = ['1.txt', '2.txt','3.txt','4.txt']
name = []

for i in range(len(l)):

    name.append(f'{i+1}.txt')

    create.create_grid(l[i], h, n_l[i], n_h, force, name[i])
    file = name[i]
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
