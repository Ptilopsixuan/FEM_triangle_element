import numpy as np
import os

def create_grid(l: list[float], h: list[float], n_l: int, n_h: int, force: float, name: str, const: list[float]):
    # 生成x轴和y轴的坐标点
    x = np.linspace(0, l, n_l)
    y = np.linspace(0, h, n_h)

    # 创建网格坐标（每个x对应所有y）
    xx, yy = np.meshgrid(x, y, indexing='ij')
    coordinates = np.column_stack((xx.ravel(), yy.ravel()))

    # 添加编号并格式化输出
    points = ""
    for idx, (x_val, y_val) in enumerate(coordinates, 1):
        points += f"{idx}, {x_val:.1f}, {y_val:.1f}\n"
        #print(f"{idx}, {x_val:.1f}, {y_val:.1f}")

    # 生成单元列表
    units = []
    for i in range(n_l - 1):  # x方向索引
        for j in range(n_h - 1):  # y方向索引
            # 计算四个顶点编号
            A = i * n_h + j + 1
            B = A + 1
            C = (i + 1) * n_h + j + 1
            D = C + 1
            
            # 创建两个三角形单元（逆时针顺序）
            units.append([A, C, B])  # 三角形1
            units.append([D, B, C])   # 三角形2

    # 生成带编号的输出
    output = []
    for unit_id, nodes in enumerate(units, 1):
        output.append([unit_id] + nodes + [1, 1])

    u = ""
    for row in output[:]:
        u += f"{row[0]:3},{row[1]:3},{row[2]:3},{row[3]:3},{row[4]},{row[5]}\n"
        #print(f"{row[0]:3},{row[1]:3},{row[2]:3},{row[3]:3},{row[4]},{row[5]}")


    start = f"{len(coordinates)} #节点数目和节点坐标：编号  x坐标  y坐标\n"
    mid = f"1 #材料信息 ：弹性模量  泊松比\n\
1 {const[0]}  {const[1]}\n\
1 # 截面信息：编号  厚度\n\
1 {const[2]}\n\
{len(output)} #单元信息：单元编号 i点 j点 m点 材料号  截面号\n"
    end = f"1#荷载信息 ：节点号，x方向力，y方向力\n\
{n_h},{force},0\n\
3#位移约束信息：节点号，约束方向，约束值\n\
1,1,0;\n\
1,2,0\n\
{(n_l-1)*n_h+1},2,0;"
    txt = start + points + mid + u + end

    os.makedirs("./input", exist_ok=True)
    path = f"./input/{name}"
    with open(path, "w", encoding="utf8") as file:
        file.write(txt)
    print(path)
    
    return None

if __name__ == "__main__":
    l = [0.4]
    n_l = [4 + 1]
    h = 4
    n_h = 40 + 1
    force = 1e6
    name = '1_1.txt'
    const = [3e10, 0.2, 0.4]
    for i in range(len(l)):
        create_grid(l[i], h, n_l[i], n_h, force, name, const)