import numpy as np
from . import type


# 计算单元刚度矩阵
def calculateKe(unit: type.Unit) -> np.ndarray:
    x = (unit.i.x, unit.j.x, unit.m.x)
    y = (unit.i.y, unit.j.y, unit.m.y)
    E = unit.material.E
    v = unit.material.v
    t = unit.plane.thickness

    # 请在这里完成单元刚度矩阵的编制
    Ke = np.zeros((6, 6))
    # 代码完善如下：
    a = [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]
    b = [y[1]-y[2], y[2]-y[0], y[0]-y[1]]
    c = [-x[1]+x[2], -x[2]+x[0], -x[0]+x[1]]

    v0 = (1-v)/2
    for i in range(0, 3):
        for j in range(0, 3):
            Ke[2*i][2*j] = b[i]*b[j]+v0*c[i]*c[j]
            Ke[2*i+1][2*j] = v*c[i]*b[j]+v0*b[i]*c[j]
            Ke[2*i][2*j+1] = v*b[i]*c[j]+v0*c[i]*b[j]
            Ke[2*i+1][2*j+1] = c[i]*c[j]+v0*b[i]*b[j]

    A = (a[0]+a[1]+a[2])/2
    k = E*t/4/A/(1-v*v)

    return Ke*k


# 集成总刚度矩阵
def integrateKe(unit: type.Unit, Kg: np.ndarray) -> None:
    Ke = unit.Ke
    i, j, m = unit.i, unit.j, unit.m
    id = [(i.id-1)*2, i.id*2-1, (j.id-1)*2, j.id*2-1, (m.id-1)*2, m.id*2-1]

    for p in range(0, 6):
        for q in range(0, 6):
            Kg[id[p]][id[q]] += Ke[p][q]


# 单元等效节点载荷列阵
def claculatePe(unit: type.Unit):
    '''
    本次练习，这个函数暂不需实现
    '''

    return None


# 单元等效节点载荷列阵
def integratePe(payloads: list[type.Payload], mid: np.ndarray):

    for p in payloads:
        id = p.point.id
        mid[(id-1)*2] += p.px
        mid[id*2-1] += p.py

    return None


# 引入位移边界条件
def integrateX(constraint: list[type.Constraint], K, P):
    '''
    采用对角元素大数法引入位移边界条件
    '''
    max = np.max(K)*6e23
    for cst in constraint:
        if (cst.value != 0):
            continue
        id = cst.point.id
        axis = int(cst.axis % 2)
        n = (id-1)*2-axis+1
        K[n][n] *= max
        # P[n] = K[n][n]*cst.value
        P[n] = 0

    return None


# def calculateA(out: type.OutputData) -> np.ndarray:
#     u, s, v = np.linalg.svd(out.K, full_matrices=False)
#     inv = np.matmul(v.T*1/s, u.T)

#     return np.matmul(inv, out.P.T)


# 解方程
def calculateA(mid: type.MidData) -> np.ndarray:
    inv = np.linalg.inv(mid.K)
    P = mid.P.T
    tmp = np.matmul(inv, P).T
    mid.a = [np.round(x, 12) for x in tmp]
    return mid.a

# 计算应变
def calculateStrain(unit: type.Unit):
    x = (unit.i.x, unit.j.x, unit.m.x)
    y = (unit.i.y, unit.j.y, unit.m.y)

    # 请在这里完成单元刚度矩阵的编制
    B = np.zeros((3, 6))
    # 代码完善如下：
    a = [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]
    b = [y[1]-y[2], y[2]-y[0], y[0]-y[1]]
    c = [-x[1]+x[2], -x[2]+x[0], -x[0]+x[1]]

    A = (a[0]+a[1]+a[2])/2

    for i in range(0, 3):
        B[0][2*i] = b[i] / 2 / A
        B[1][2*i+1] = c[i] / 2 / A
        B[2][2*i] = c[i] / 2 / A
        B[2][2*i+1] = b[i] / 2 / A 

    ae = [unit.i.ax, unit.i.ay, unit.j.ax, unit.j.ay, unit.m.ax, unit.m.ay]
    unit.e = np.matmul(B, ae).tolist()

    return True

# 计算应力
def calculateStress(unit: type.Unit):
    E = unit.material.E
    v = unit.material.v

    # 请在这里完成单元刚度矩阵的编制
    D = np.zeros((3, 3))
    # 代码完善如下：
    D[0][0] = 1
    D[0][1] = v 
    D[1][0] = v 
    D[1][1] = 1
    D[2][2] = (1-v) / 2 

    D = D * E / (1 - v * v)

    unit.s = np.matmul(D, unit.e).tolist()

    return True

# 生成输出数据
def gennerate(data: type.MidData):
    points = data.data.points
    for i in range(0, len(points)):
        points[i].ax, points[i].ay = data.a[i*2], data.a[i*2+1]
    
    for unit in data.data.units:
        # 计算应变
        calculateStrain(unit)
        # 计算应力
        calculateStress(unit)

    return type.OutputData(points, data.data.units)
