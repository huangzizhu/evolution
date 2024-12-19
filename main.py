from  Map import Map
import evolution as ev
import os
import other
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# 初始化参数
max_generations = 100  # 最大迭代代数
max_achivement = 10
fitness_values = []    # 适应度值的列表
generations = []       # 代数的列表



# 创建图形和坐标轴
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)  # 初始化线条
ax.set_xlim(0, max_generations)  # 设置x轴范围
ax.set_ylim(0, max_achivement)  # 设置y轴范围（根据适应度范围调整）
ax.set_xlabel('迭代次数')
ax.set_ylabel('Fitness')
ax.set_title('Fitness over Generations')

# 动态更新函数
def update(frame,pop):
    # 模拟适应度的变化（这里用随机数代替实际的适应度计算）
    global max_generations
    global max_achivement
    other.round(pop)
    achivement = pop.achivement
    if frame < max_generations and achivement < max_achivement:
        fitness_values.append(achivement + max_achivement - 10)
        generations.append(frame + max_generations - 100)

        # 更新线条数据
        line.set_data(generations, fitness_values)

        # 动态调整x轴刻度
        ax.set_xlim(0, frame + 10)  # 让x轴范围随着代数动态变化
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # 确保x轴刻度为整数

    else:
        if frame >= max_generations:
            fitness_values.clear()
            generations.clear()
            max_generations += 100
            print("clcl")
        else :
            max_achivement += achivement
    return line,

map = Map()


def main():
    # 获取当前工作目录
    current_directory = os.getcwd()
    #准备
    pop = other.prepare(map)
    #开始进行每轮
    while(1):
        achivement = pop.achivement
        other.round(pop)
        # 创建动画
    #ani = FuncAnimation(fig, update, frames=max_generations, fargs=(pop,), interval=10)
        # 显示图形
    #plt.show()
        now_achivement = pop.achivement
        if(now_achivement == 1000):
            break

if __name__ == "__main__":
    main()





