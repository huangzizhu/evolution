import  random
import os
import multiprocessing
from Map import Map
import other


#个体类
class Individual:
    def __init__(self,Map:Map):
        self.map = Map.map#map数据
        self.layer = Map.layer#层数
        self.dna:str = ""#dna信息1000长度的字符串
        self.achivement:int = 0#成就
        self.time = 0
    #用于首次生成第一代的dna
    def init(self):
        list_res = []
        #随机生成经过的门
        for i in range(1000):
            list_res.append(str(random.randint(0,9)))
        #写入dna
        self.dna =  "".join(list_res)
    #读取dna
    def read(self,str_dna:str):
        self.dna = str_dna
    #评估该个体在map中的得分
    def evaluate(self):
        #计算方法，由两个方面组成，走的距离和速度,权重随achivement（当前走到的步数）变化
        #距离，离出口的距离 速度，纵向移动和横向移动都会消耗1个tick ，走到终点或者死亡所花费的tick数
        achivement = self.achivement
        #rate_distance = 0.2 + 0.6 * (1 - (achivement / self.layer))  #distance所占权重 0.2基础+
        #rate_time = 1 - rate_distance #time所占权重 0.2基础+
        distance = 0
        time = 0
        last_door = int((self.dna[0]))#上一个门的编号
        #每层遍历判断
        for i in range(self.layer):
            if self.dna[i] in self.map[i]:
                distance += 1
                time += abs(int(self.dna[i]) - last_door)
                last_door = int(self.dna[i])
            else:
                break
        #适应度计算： 权重 * 当前走的距离 / 总距离 +  (1 - 当前消耗时间 / (10 * 当前走的距离)) * 权重

        #fitnes_distance = rate_distance * distance
        #fitnes_time = (1 - time / (10 * distance)) * rate_time
        self.achivement = distance
        self.time = time
        #self.fitness =  distance

#种群类
class Population:
    def __init__(self,Map:Map):
        self.count = 1#迭代数
        self.Map = Map
        self.quantity = 100#种群数量
        self.individuals = []#个体集合
        self.achivement = 0#当前种群的最快进度


    #生成第一代种群
    def init(self):
        for i in range(self.quantity):
            #生成quantity个个体并随机分配dna以形成第一代种群
            individual = Individual(self.Map)
            individual.init()
            #将每个个体加入到个体集合中
            self.individuals.append(individual)
        self.count += 1
    #将种群数据写入到文件
    def write(self):
        # 获取当前工作目录
        current_directory = os.getcwd()
        path_folder_generation = os.path.join(current_directory, "generation")
        # generation文件存在，读取，不存在，生成并写入
        try:
            os.makedirs(path_folder_generation)
            print(f"文件夹 generation 创建成功！")
        except FileExistsError:
            print(f"文件夹 generation 已经存在。")
        except Exception as e:
            print(f"创建文件夹时发生错误: {e}")
        path_file_data = path_folder_generation + f"\\{self.count}.data"

        if os.path.exists(path_file_data):
            print(f"{self.count}.data存在，开始写入")
            with open(path_file_data,"w",encoding="utf-8") as f:
                for line in self.individuals:
                    f.write(line.dna+"\n")
            print("写入完成")
        else:
            print(f"{self.count}.data不存在，正在生成并写入")
            with open(path_file_data,"w",encoding="utf-8") as f:
                for line in self.individuals:
                    f.write(line.dna+"\n")
            print("生成并写入完成")
    #将种群数据从文件中读取
    def read(self):
        # 获取当前工作目录
        current_directory = os.getcwd()
        path_folder_generation = os.path.join(current_directory, "generation")
        path_file_data = path_folder_generation + f"\\{self.count}.data"
        with open(path_file_data,"r",encoding="utf-8") as f:
            for line in f:
                individual = Individual(self.Map)
                individual.dna = line.strip()
                self.individuals.append(individual)

    #对每个个体进行计算
    def caculate(self):
        for individual in self.individuals:
            #计算每个个体的适应度
            individual.achivement = self.achivement#先修改为种群整体的最大achi
            individual.evaluate()
    #对种群进行筛选
    def select(self):
        '''# 先按照achivement排序
        self.individuals.sort(key=lambda Individual: Individual.achivement, reverse=True)
        # 更新achivement
        self.achivement = self.individuals[0].achivement
        # 按照fitness排序
        self.individuals.sort(key=lambda Individual: Individual.fitness, reverse=True)'''
        # 先按照achivement排序，在achivement相同的情况下根据fitness排序
        self.individuals.sort(key=lambda Individual: (-Individual.achivement, -Individual.time))
        # 更新achivement
        self.achivement = self.individuals[0].achivement
        # 去除后面一半
        del self.individuals[-(self.quantity // 2):]

    #染色体交叉
    def cross(self):
        len_cut = 20#每个dna切片长度
        random.shuffle(self.individuals)#随机打乱
        for i in range(self.quantity//4):#两两配对
            f1 = self.individuals[i*2]
            f2 = self.individuals[i*2+1]
            son1 = Individual(self.Map)
            son2 = Individual(self.Map)
            dna1 = ""
            dna2 = ""
            for j in range(son1.layer // len_cut):
                choice = random.randint(0,1)
                #choice == 0 ,f1 -> son1 , f2 -> son2
                if choice == 0:
                    dna1 += f1.dna[len_cut*j:len_cut*(j+1)]
                    dna2 += f2.dna[len_cut*j:len_cut*(j+1)]
                else:#choice == 1 ,f1 -> son2 , f2 -> son3
                    dna2 += f1.dna[len_cut * j:len_cut * (j + 1)]
                    dna1 += f2.dna[len_cut * j:len_cut * (j + 1)]
            son1.dna = dna1
            son2.dna = dna2
            self.individuals.append(son1)
            self.individuals.append(son2)

    #基因突变
    def mutate(self):
        rate_mutation = 0.01
        for individual in self.individuals:
            for i in range(self.achivement,len(individual.dna)):
                if(random.randint(1,1000) == 80):
                    individual.dna = individual.dna[:i] + str(random.randint(0,9)) + individual.dna[i+1:]









