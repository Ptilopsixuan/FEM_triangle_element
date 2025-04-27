import numpy as np


class Point: # 节点
    id = 0
    # 坐标
    x = 0
    y = 0
    # 荷载
    px = 0
    py = 0
    # 位移
    ax = 0
    ay = 0

    def __init__(self, data: list[float]) -> None:
        (self.id, self.x, self.y) = data

    def __str__(self) -> str:
        return f"<id:{self.id}, x:{self.x}, y:{self.y}>"

    def __repr__(self) -> str:
        return self.__str__()


class Material: # 材料
    id = 0
    E = 0
    v = 0

    def __init__(self, data: list[float]) -> None:
        (self.id, self.E, self.v) = data

    def __str__(self) -> str:
        return f"<id:{self.id}, E:{self.E}, v:{self.v}>"

    def __repr__(self) -> str:
        return self.__str__()


class Plane: # 截面
    id = 0
    thickness = 0

    def __init__(self,  data: list[float]) -> None:
        (self.id, self.thickness) = data

    def __str__(self) -> str:
        return f"<id:{self.id}, thickness:{self.thickness}>"

    def __repr__(self) -> str:
        return self.__str__()


class Unit: # 单元
    id = 0
    i: Point = None
    j: Point = None
    m: Point = None
    material: Material = None
    plane: Plane = None

    # 单元刚度矩阵
    Ke = None

    def __init__(self, data: list) -> None:
        (self.id, self.i, self.j, self.m, self.material, self.plane) = data

    def __str__(self) -> str:
        return f"<id:{self.id}, i:{self.i.id}, j:{self.j.id}, m:{self.m.id}, material:{self.material.id}, plane:{self.plane.id}>"

    def __repr__(self) -> str:
        return self.__str__()


class Payload: # 荷载
    point: Point = None
    px = 0
    py = 0

    def __init__(self, data: list) -> None:
        (self.point, self.px, self.py) = data

    def __str__(self) -> str:
        return f"<point:{self.point.id}, px:{self.px}, py:{self.py}>"

    def __repr__(self) -> str:
        return self.__str__()


class Constraint:
    point: Point = None
    axis = 1
    value = 0

    def __init__(self, data: list) -> None:
        (self.point, self.axis, self.value) = data

    def __str__(self) -> str:
        return f"<point:{self.point.id}, axis:{self.axis}, value:{self.value}>"

    def __repr__(self) -> str:
        return self.__str__()


def f(str: str):
    return not str.isspace()


def strToFloat(str: str, sep=','):
    tmp = []
    for i in str.split(sep):
        if not i.strip() == '':
            tmp.append(float(i))


class InputData:
    points: list[Point] = []
    planes: list[Plane] = []
    units: list[Unit] = []
    materials: list[Material] = []
    payloads: list[Payload] = []
    constraints: list[Constraint] = []

    def __init__(self) -> None:
        self.points, self.planes, self.units, self.materials, self.payloads, self.constraints = [], [], [], [], [], []

    def __str__(self) -> str:
        return f"<\npoints:{self.points},\nplanes:{self.planes},\nunits:{self.units},\nmaterials:{self.materials},\npayloads:{self.payloads},\nconstraints:{self.constraints}\n>"

    def __repr__(self) -> str:
        return self.__str__()


class MidData:
    data: InputData = None
    # 结构总刚度矩阵
    K: np.ndarray = []

    # 载荷列向量
    P: np.ndarray = []

    # 位移向量
    a: np.ndarray = []

    def __init__(self, data: InputData) -> None:
        self.data = data


class OutputData:
    points = []

    def __init__(self, points:list[Point]) -> None:
        self.points = points
