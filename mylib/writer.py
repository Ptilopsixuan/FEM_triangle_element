from . import type, draw

def writeFile(path: str, output: type.OutputData):

    draw.d(output)
    
    try:
        with open(path, "w", encoding="utf8") as file:
            for p in output.points:
                file.write(
                    f"ponit: {p.id}:({p.x:0.3f}, {p.y:0.3f}),\t displacement: x->{p.ax:0.3e}, y->{p.ay:0.3e};\n")

    except Exception as e:
        print(e, '\n文件输出失败')
