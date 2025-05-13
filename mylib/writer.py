from . import type, draw

def writeFile(path: str, output: type.OutputData):

    pic_path = path.replace(".txt", ".png")
    draw.d(output, pic_path)
    
    try:
        with open(path, "w", encoding="utf8") as file:
            for p in output.points:
                # if p.id == 41 or p.id == len(output.points):
                    file.write(
                        f"ponit: {p.id}:({p.x:0.3f}, {p.y:0.3f}),\t displacement: x: {p.ax:0.3e}, y: {p.ay:0.3e};\n")
                    # with open("./result.txt", "a", encoding="utf8") as fr:
                    #     fr.write(f"{p.ax:0.3e}, {p.ay:0.3e}\n")
            for unit in output.units:
                file.write(
                    f"unit: {unit.id}, strain: {unit.e[0]:0.3e}, {unit.e[1]:0.3e}, {unit.e[2]:0.3e}, stress: {unit.s[0]:0.3e}, {unit.s[1]:0.3e}, {unit.s[2]:0.3e}\n")
                


    except Exception as e:
        print(e, '\n文件输出失败')
