import numpy as np
import os
from mylib import type, operator, reader, writer, create

'''平面应力'''
l = [2]
n_l = []
for i in range(len(l)):
    n_l.append(int(l[i] / 0.5) + 1)
h = 3
n_h = (int)(3 / 0.5 + 1)
force = 1e8
const = [3e10, 0.2, 0.24]    # E, v, t 

name = []

for i in range(len(l)):

    name.append(f'{i+1}.txt')

    create.create_grid(l[i], h, n_l[i], n_h, force, name[i], const)
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
