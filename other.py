from  Map import Map
import evolution as ev
import os


ifmap = 0#map文件是否存在
count = 0#进行到第几轮
achivement = 0#当前进度





#写入map（第一次生成map时使用）
def write_map(map:Map):
    #生成map
    map.init()
    # 定义要创建的文件夹名称
    folder_name = 'map'
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 创建完整的文件夹路径
    path_folder_map = os.path.join(current_directory, folder_name)
    # 创建文件夹，如果文件夹已经存在，会抛出异常
    try:
        os.makedirs(path_folder_map)
        print(f"文件夹 '{folder_name}' 创建成功！")
    except FileExistsError:
        print(f"文件夹 '{folder_name}' 已经存在。")
    except Exception as e:
        print(f"创建文件夹时发生错误: {e}")
    map.write(path_folder_map)

#读取map，从map.data中读取map数据
def read_map(path_file:str,map:Map):
    map.read(path_file)

#写入当前信息
def write_statu(ifmap,count,achivement):
    print(f'正在保存当前进度info:{achivement}')
    # 获取当前工作目录
    current_directory = os.getcwd()
    with open(current_directory+"\\info",'w',encoding="utf-8") as f:
        f.write(str(ifmap)+"\n")
        f.write(str(count)+"\n")
        f.write((str(achivement)))
    print("保存成功！")
#读取上次运行的信息 返回值list 第一个是ifmap 第二个是count
def read_statu():
    # 获取当前工作目录
    current_directory = os.getcwd()
    list_res = [] #结果
    #info文件路径
    path_file_info = current_directory+"\\info"
    if os.path.exists(path_file_info):
        with open(path_file_info,"r",encoding="utf-8") as f:
            for line in f:
                list_res.append(int(line.strip()))
     #info 信息不存在，写入0
    else:
        print("info文件不存在，正在创建并初始化")
        write_statu(0,0,0)
        return read_statu()
    print("info读取完成")
    return  list_res


#准备
def prepare(map:Map):
    # 获取当前工作目录
    current_directory = os.getcwd()
    #-------------获取上次的运行信息----------------
    list_info =  read_statu()
    global ifmap
    ifmap = list_info[0]
    global count
    count = list_info[1]
    global  achivement
    achivement = list_info[2]
    # -------------获取上次的运行信息----------------

    #——————————————————————————————————读取map————————————————————————
    # map文件夹路径
    path_folder_map = os.path.join(current_directory, "map")
    path_file_map = path_folder_map + '\\map.data'
    # map文件存在，读取，不存在，生成并写入
    if os.path.exists(path_file_map) and ifmap:
        print("map.data存在，开始读取")
        read_map(path_file_map, map)
        print("读取完成")
    else:
        print("map.data不存在，正在生成并写入")
        write_map(map)
        ifmap = 1
        print("生成并写入完成")
    # ——————————————————————————————————读取map————————————————————————
    #------------------------------读取种群信息--------------------------
    print("正在读取种群信息")
    pop = ev.Population(map)
    pop.count = count #修改代数
    pop.achivement = achivement#修改进度
    #如果轮数为0，进行第一代生成并写入
    if count  == 0:
        print("尚无信息，开始生成第一代")
        pop.init()
        pop.write()
        count = pop.count
        write_statu(ifmap,count,achivement)
        print(f"生成成功,代数:{pop.count},保存至{pop.count}.data")
    print(f"正在读取，当前代数{pop.count}，当前成就{pop.achivement}")
    pop.read()#读取
    print("种群信息读取成功，一切就绪！")
    #------------------------------读取种群信息--------------------------
    return  pop

def round(pop):
    #计算适应度
    pop.caculate()
    #排序筛选
    pop.select()
    #染色体交叉
    pop.cross()
    #突变
    pop.mutate()
    #写入文件
    pop.write()
    #写入info
    write_statu(ifmap,pop.count,pop.achivement)
    #计数
    pop.count += 1
