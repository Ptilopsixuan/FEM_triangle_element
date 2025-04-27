import numpy as np
import os
from mylib import type, operator, reader, writer, create

# files = os.listdir('.\\input')
# for file in files:
l = [0.4, 0.8, 1.6, 3.2]
n_l = [4 + 1, 8 + 1, 16 + 1, 32 + 1]
h = 4
n_h = 40 + 1
force = 1e6
name = ['1_1.txt', '2_1.txt','3_1.txt','4_1.txt']

for i in range(len(l)):
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
