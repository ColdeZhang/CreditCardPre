'''
Created on 2020年11月17日

@author: My
'''
import xlrd
import operator
import tkinter
from tkinter import Button,PanedWindow
from math import log
import DTreePlot
import OffenceView
import SearchCrimerView;



class Window(object):
    def __init__(self, init_Window):
        self.init_Window=init_Window
        
    def initWindow(self, showDesignTree):
        self.crime_to_law={
           '无罪':'主要法律依据\r\n中华人民共和国刑事诉讼法第二百条',
           '信用卡诈骗罪':'主要法律依据\r\n中华人民共和国刑法第一百九十六条\r\n伪造、冒用、恶意透支\r\n其他法律依据\r\n最高人民法院、最高人民检察院古关于办理诈骗刑事案件适用法律问题的若干解释',
           '骗取贷款罪' :'主要法律依据\r\n中华人民共和国刑法第一百七十五条之一\r\n欺骗手段，其他法律依据\r\n最高人民法院、最高人民检察院古关于办理诈骗刑事案件具体应用法律的若干问题的解释',
           '妨害信用卡管理罪':'主要法律依据\r\n中华人民共和国刑法第二百六十六条\r\n数量较大、交易\r\n其他法律依据\r\n最高人民法院、最高人民检察院古关于办理诈骗刑事案件具体应用法律的若干问题的解释', 
           '非法经营罪':'主要法律依据\r\n中华人民共和国刑法第二百二十五条\r\n数量较大、交易\r\n其他法律依据\r\n最高人民法院、最高人民检察院古关于办理非法从事资金支付结算业务、非法买卖外汇刑事案件适用法律若干问题的解释',
           '盗窃罪':'未知，待补充'}
        
        self.showDesignTree=showDesignTree
        
        self.dataSet=[]
        self.olds=[]    # 年龄
        self.eduLevel=[]    # 教育水平
        self.jobs=[]    # 职业
        self.cashOutBehavior=[] #   行为
        self.consuGoals=[]
        self.proofs=[]
        self.crimes=[]
        self.crime_to_records={}
        self.featureNum=7
        self.featrueBIndex=1
        self.featrueEIndex=7
        self.dataItemNum=9
        
        
        self.xlsDataSet=xlrd.open_workbook("./data/data.xlsx")
        self.dataSetSheet = self.xlsDataSet.sheets()[0]
        nrows = self.dataSetSheet.nrows
        for index in range(0,nrows):
            if index==0:
                self.labels=[str(self.dataSetSheet.cell(index,cindex).value).replace(" ", "") for cindex in range(1,self.featrueEIndex+2)]
            else :
                self.dataSet.append([])
                self.dataSet[index-1]=[str(self.dataSetSheet.cell(index,cindex).value).replace(" ", "").replace(".0","") for cindex in range(1,self.featrueEIndex+2)]
                if str(self.dataSetSheet.cell(index, 2).value).replace(" ", "") not in self.olds:
                    self.olds.append(str(self.dataSetSheet.cell(index, 2).value).replace(" ", ""))
                if str(self.dataSetSheet.cell(index, 3).value).replace(" ", "") not in self.eduLevel:
                    self.eduLevel.append(str(self.dataSetSheet.cell(index, 3).value).replace(" ", ""))
                if str(self.dataSetSheet.cell(index, 4).value).replace(" ", "") not in self.jobs:
                    self.jobs.append(str(self.dataSetSheet.cell(index, 4).value).replace(" ", ""))
                if str(self.dataSetSheet.cell(index, 5).value).replace(" ", "") not in self.cashOutBehavior:
                    self.cashOutBehavior.append(str(self.dataSetSheet.cell(index, 5).value).replace(" ", ""))
                if str(self.dataSetSheet.cell(index, 6).value).replace(" ", "") not in self.consuGoals:
                    self.consuGoals.append(str(self.dataSetSheet.cell(index, 6).value).replace(" ", ""))
                if str(self.dataSetSheet.cell(index, 7).value).replace(" ", "") not in self.proofs:
                    self.proofs.append(str(self.dataSetSheet.cell(index, 7).value).replace(" ", ""))
                if str(self.dataSetSheet.cell(index, 8).value).replace(" ", "") not in self.crimes:
                    self.crimes.append(str(self.dataSetSheet.cell(index, 8).value).replace(" ", ""))
 
        for index in range(1,nrows):
            crime=str(self.dataSetSheet.cell(index, 8).value).replace(" ", "")
            if crime not in self.crime_to_records.keys():self.crime_to_records[crime]=[]
            self.crime_to_records[crime].append(" ".join(   ["%-15s"%(str(self.dataSetSheet.cell(index,cindex).value).replace(" ", "")) for cindex in range(1,self.featrueEIndex+1)]  ))
           
        self.olds= [i for i in list(set(self.olds)) if(len(str(i))!=0)]     
        self.eduLevel= [i for i in list(set(self.eduLevel)) if(len(str(i))!=0)]
        self.jobs= [i for i in list(set(self.jobs)) if(len(str(i))!=0)]
        self.cashOutBehavior= [i for i in list(set(self.cashOutBehavior)) if(len(str(i))!=0)]
        self.consuGoals= [i for i in list(set(self.consuGoals)) if(len(str(i))!=0)]
        self.proofs= [i for i in list(set(self.proofs)) if(len(str(i))!=0)]
        self.crimes= [i for i in list(set(self.crimes)) if(len(str(i))!=0)]
          
        self.init_Window.title("信用卡套现正反双向检索系统")
        screenwidth = self.init_Window.winfo_screenwidth()
        screenheight = self.init_Window.winfo_screenheight()
        size = '%dx%d+%d+%d' % (1124, 768, (screenwidth - 1124)/2, (screenheight - 768)/2)
        self.init_Window.geometry(size)
        self.init_Window.maxsize(1124, 768)
        self.init_Window.minsize(1124, 768)
        self.init_Window.protocol("WM_DELETE_WINDOW", self.onClosing)
        
        self.headPanel=PanedWindow(self.init_Window,orient="horizontal",borderwidth=1,relief="raised", width=1123, height=30)
        self.headPanel.pack(fill="x")
        self.offenceViewButton=Button(self.init_Window,text="犯罪预测视图",width=80,command=self.offenceViewClicked)
        self.headPanel.add(self.offenceViewButton)
        self.searchCrimerViewButton=Button(self.init_Window,text="罪犯检索视图",width=80,command=self.searchCrimerViewClicked)
        self.headPanel.add(self.searchCrimerViewButton)
        
        self.offenceView=OffenceView.CrimeView(self)
        self.searchCrimerView=None
        
        self.dtree=self.createTree(self.dataSet, self.getFeatureLabel())
        
        if self.showDesignTree:
            DTreePlot.create_plot(self.dtree) #生成可视化的决策树
        
    def onClosing(self):
        self.init_Window.destroy()
        
    def getInitWindow(self):
        return self.init_Window
    
    def getDTree(self):
        return self.dtree
    
    def getCrime_to_law(self):
        return self.crime_to_law
    
    def getCrime_to_records(self): 
        return self.crime_to_records
       
    def getFeatureLabel(self):
        return [str(self.dataSetSheet.cell(0,cindex).value).replace(" ", "") for cindex in range(1,self.featrueEIndex+2)]
       
    def getOlds(self):
        return self.olds
            
    def getEduLevels(self):
        return tuple(self.eduLevel)
        
    def getJobs(self):
        return tuple(self.jobs)
    
    def getCashOutBehavior(self):
        return tuple(self.cashOutBehavior)
        
    def getConsuGoals(self):
        return tuple(self.consuGoals)
    
    def getProofs(self):
        return tuple(self.proofs)
    
    def getCrimes(self):
        return tuple(self.crimes)
        
    def offenceViewClicked(self):
        if(self.searchCrimerView):
            self.searchCrimerView.destroy()
            self.searchCrimerView=None
            
        if(not self.offenceView):
            self.offenceView=OffenceView.CrimeView(self)
        
    def searchCrimerViewClicked(self):
        if(self.offenceView):
            self.offenceView.destroy()
            self.offenceView=None
             
        if(not self.searchCrimerView):
            self.searchCrimerView=SearchCrimerView.CrimerView(self)
    
    #计算信息熵
    def calcShannonEnt(self,dataSet):
        numEntries = len(dataSet)  # 样本数
        labelCounts = {}   # 创建一个数据字典：key是最后一列的数值（即标签，也就是目标分类的类别），value是属于该类别的样本个数
        for featVec in dataSet: # 遍历整个数据集，每次取一行
            currentLabel = featVec[-1]  #取该行最后一列的值
            if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1
        shannonEnt = 0.0  # 初始化信息熵
        for key in labelCounts:
            prob = float(labelCounts[key])/numEntries
            shannonEnt -= prob * log(prob,2) #log base 2  计算信息熵
        return shannonEnt
               
    #按给定的特征划分数据
    def splitDataSet(self, dataSet, featureItemIndex, featureValue):
        retDataSet = []
        for featVec in dataSet:
            if featVec[featureItemIndex]==featureValue:
                reducedFeatVec = featVec[:featureItemIndex]     #chop out axis used for splitting
                reducedFeatVec.extend(featVec[featureItemIndex+1:])
                retDataSet.append(reducedFeatVec)
        return retDataSet
    
    #选取当前数据集下，用于划分数据集的最优特征
    def chooseBestFeatureToSplit(self,dataSet):
        bestFeature=-1;bestInfoGain=0.0
        numFeatures = len(dataSet[0]) - 1
        nrows=len(dataSet)
        shannonEnt=self.calcShannonEnt(dataSet)
        for cindex in range(numFeatures):
            featureList=[example[cindex] for example in dataSet]
            featureList= [i for i in list(set(featureList)) if(len(str(i))!=0)]
            newShannonEnt = 0.0
            for value in featureList:
                subDataSet=self.splitDataSet(dataSet, cindex, value)
                prob = len(subDataSet)/float(nrows)
                newShannonEnt += prob * self.calcShannonEnt(subDataSet)
            infoGain=shannonEnt-newShannonEnt
            if infoGain>bestInfoGain:
                bestInfoGain=infoGain
                bestFeature=cindex
        return bestFeature
            
    #该函数使用分类名称的列表，然后创建键值为classList中唯一值的数据字典。字典
    #对象的存储了classList中每个类标签出现的频率。最后利用operator操作键值排序字典，
    #并返回出现次数最多的分类名称
    def majorityCnt(self,classList):
        classCount={}
        for fetureT in classList:
            if fetureT not in classCount.keys(): classCount[fetureT] = 0
            classCount[fetureT] += 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]

    # 生成决策树主方法
    def createTree(self, dataSet, labels):
        classList = [example[-1] for example in dataSet]
            
        if classList.count(classList[0]) == len(classList):
            return classList[0]#当类别完全相同时则停止继续划分，直接返回该类的标签
        if len(dataSet[0]) == 1: ##遍历完所有的特征时，仍然不能将数据集划分成仅包含唯一类别的分组 dataSet
            return self.majorityCnt(classList) #由于无法简单的返回唯一的类标签，这里就返回出现次数最多的类别作为返回值
        bestFeat = self.chooseBestFeatureToSplit(dataSet) # 获取最好的分类特征索引
        bestFeatLabel = labels[bestFeat] #获取该特征的名字
    
        # 这里直接使用字典变量来存储树信息，这对于绘制树形图很重要。
        myTree = {bestFeatLabel:{}} #当前数据集选取最好的特征存储在bestFeat中
        del(labels[bestFeat]) #删除已经在选取的特征
        featValues = [example[bestFeat] for example in dataSet]
        uniqueVals = set(featValues)
        for value in uniqueVals:
            subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
            myTree[bestFeatLabel][value] = self.createTree(self.splitDataSet(dataSet, bestFeat, value),subLabels)
        return myTree
    
    def classify(self, inputTree, featureLabel, testVec):
        classLabel="此犯罪记录未被收入决策系统"
        for index in range(len(inputTree.keys())):
            firstStr = list(inputTree.keys())[index]
            secondDict = inputTree[firstStr]
            featIndex = featureLabel.index(firstStr)
            key = testVec[featIndex]
            if key in secondDict.keys():
                valueOfFeat = secondDict[key]
                if isinstance(valueOfFeat, dict): 
                    classLabel = self.classify(valueOfFeat, featureLabel, testVec)
                else: 
                    classLabel = valueOfFeat
                break
            
        return classLabel
    
    def storeTree(self, filename):
        import pickle
        fw = open(filename,'w')
        pickle.dump(self.dtree,fw)
        fw.close()
    
    def grabTree(self, filename):
        import pickle
        fr = open(filename)
        return pickle.load(fr)

# if __name__ == '__main__':
#     start(MyApp, address='0.0.0.0', port=11111, multiple_instance=True)
    # top=tkinter.Tk()
    # main_window=Window(top)
    # main_window.initWindow(False);
    # top.mainloop();