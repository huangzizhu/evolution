import os
import other
import Map
import evolution as ev
import matplotlib.pyplot as plt
import multiprocessing
from functools import partial


map = Map.Map()
ifmap = 0#map文件是否存在
count = 0#进行到第几轮
achivement = 0#当前进度
dir_now = os.getcwd()
dir_generation = dir_now + '\\generation'
#遍历当前目录下所有文件
def get_files_in_directory(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def prepare(map):
    list_info = other.read_statu()
    global ifmap
    ifmap = list_info[0]
    global count
    count = list_info[1]
    global achivement
    achivement = list_info[2]
    # ——————————————————————————————————读取map————————————————————————
    # map文件夹路径
    path_folder_map = os.path.join(dir_now, "map")
    path_file_map = path_folder_map + '\\map.data'
    # map文件读取
    other.read_map(path_file_map, map)


def read_file(pop):
    # ------------------------------读取种群信息--------------------------
    pop.read()  # 读取
    # ------------------------------读取种群信息--------------------------
    pop.caculate()#计算
    pop.select()#获取achivement

def worker(i,map):
    pop = ev.Population(map)
    pop.count = i + 1
    read_file(pop)
    print(f'{i + 1}代：{pop.achivement}')
    return i + 1,pop.achivement
if __name__ == '__main__':
    #all_files = get_files_in_directory(dir_generation)
    prepare(map)
    num_processes = multiprocessing.cpu_count()  # 获取 CPU 核心数
    # 使用进程池并收集返回值
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(partial(worker, map = map), range(count))  # 传递任务并收集返回值
    # 将返回值拆分成两个列表
    list_generation, list_achivement = zip(*results)  # zip(*results) 将结果拆分成两个列表
    # 创建图形
    plt.figure(figsize=(10, 6))
    plt.plot(list_generation, list_achivement, marker='o', linestyle='-', color='b')

    # 添加标题和标签
    plt.title('Evolution Progress Visualization')
    plt.xlabel('Generations')
    plt.ylabel('achivement')
    # 添加网格
    plt.grid()
    # 显示图形
    plt.show()

