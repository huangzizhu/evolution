import  concurrent.futures
import  random
import os
class Map:
    #初始化
    def __init__(self):
        self.layer:int = 1000 #层数
        self.doors:int = 10#每一层的门的数量
        self.maxOpenDoor = 3#每层最多打开的门的数量
        self.minOpenDoor = 1#每层最少打开的门的数量
        self.map:list = []#地图数据 1000个字符串
    #生成一个地图
    def init(self):
        len = 10#每段地图的长度
        parts = self.layer // len#需要多少个片段
        maxworks = 10#最大同时进行10个片段的生成
        #创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxworks) as executor:
            #提交任务
            futures = [executor.submit(self.__generate,len) for i in range(parts)]
        #等待完成并获取结果
        for future in concurrent.futures.as_completed(futures):
            #每个future返回每10层的数据，现在遍历将每一层添加到map中
            for layers_data in future.result():
                self.map.append(layers_data)
    #生成地图的每一段
    def __generate(self,len:int):
        #结果list
        list_res = []
        #依次绘制每一层
        for i in range(len):
            str_res = ""
            #每层随机打开的门的数量
            for j in range(random.randint(self.minOpenDoor,self.maxOpenDoor)):
                str_res += str(random.randint(0,self.doors-1))#向每一层的增加打开的门
            list_res.append(str_res)#添加结果
        return list_res


    #从文件中读取地图
    def read(self,path_file:str):
        print("正在读取地图信息")
        with open(path_file, "r", encoding='utf-8') as f:
            for line in f:
                self.map.append(line.strip())
        print("读取地图信息成功！")
    #将地图数据写入到文件中
    def write(self,path:str):
        print("写入地图信息")
        # 写入文件
        with open(path + "\\map.data", "w", encoding='utf-8') as f:
            for line in self.map:
                f.write(line+"\n")
        print("写入成功")
