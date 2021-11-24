import remi.gui as gui
from remi import start, App
import xlrd
import operator
import tkinter
from math import log
import DTreePlot
import OffenceView
import SearchCrimerView;
from random import choice

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.crime_to_law={
           '无罪':'主要法律依据\r\n中华人民共和国刑事诉讼法第二百条',
           '信用卡诈骗罪':'主要法律依据\r\n中华人民共和国刑法第一百九十六条\r\n伪造、冒用、恶意透支\r\n其他法律依据\r\n最高人民法院、最高人民检察院古关于办理诈骗刑事案件适用法律问题的若干解释',
           '骗取贷款罪' :'主要法律依据\r\n中华人民共和国刑法第一百七十五条之一\r\n欺骗手段，其他法律依据\r\n最高人民法院、最高人民检察院古关于办理诈骗刑事案件具体应用法律的若干问题的解释',
           '妨害信用卡管理罪':'主要法律依据\r\n中华人民共和国刑法第二百六十六条\r\n数量较大、交易\r\n其他法律依据\r\n最高人民法院、最高人民检察院古关于办理诈骗刑事案件具体应用法律的若干问题的解释', 
           '非法经营罪':'主要法律依据\r\n中华人民共和国刑法第二百二十五条\r\n数量较大、交易\r\n其他法律依据\r\n最高人民法院、最高人民检察院古关于办理非法从事资金支付结算业务、非法买卖外汇刑事案件适用法律若干问题的解释',
           '盗窃罪':'未知，待补充'}
        
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

        self.dtree=self.createTree(self.dataSet, self.getFeatureLabel())


        # 页面主框架
        mainBox = gui.TabBox(width='80%', margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})

        # 页面一
        # 模糊计算页面
        self.vagueSearch = gui.Container(width='80%',layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.vagueSearch, '模糊计算')
        self.vagueSearchInfo = gui.VBox(width='40%', margin='10px')
        self.vagueSearchPanel = gui.VBox(width='40%', margin='10px')
        self.vagueSearch.append(self.vagueSearchInfo)
        self.vagueSearch.append(self.vagueSearchPanel)

        # 模糊计算说明
        self.vagueSearchTitle = gui.Label('关于模糊计算', width='80%', style={'font-size': '20px'})
        self.vagueSearchInfo.append(self.vagueSearchTitle)
        self.vagueSearchContent = gui.Label('', width='90%', style={'font-size': '20px'})

        # 选择模型
        self.modelSelect = gui.HBox(width='90%', height=20, margin='10px auto')

        self.modelLabelText = gui.Label('当前模型：', width='40%', height=20, margin='10px')
        self.modelSelect.append(self.modelLabelText)
        
        self.modelSelectDropDown = gui.DropDown.new_from_list(('NBC', 'LR', 'SVM', 'ID3', 'C5.0', 'ANN', 'KNN'), width='60%', height=20, margin='10px')
        self.selectedModel = 'C5.0'
        self.modelSelectDropDown.select_by_value(self.selectedModel)
        self.modelSelectDropDown.onchange.do(self.selectModel_changed)
        self.modelSelect.append(self.modelSelectDropDown)

        self.vagueSearchPanel.append(self.modelSelect)

        # 输入框
        self.vagueSearchInput = gui.TextInput(width='80%', height=90, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.vagueSearchInput.set_text('请输入犯罪事实')
        self.vagueSearchPanel.append(self.vagueSearchInput)
        self.vagueSearchInput.onchange.do(self.vagueSearchInput_changed)
        self.currentVagueInput = ""
        self.previewVagueInput = ""

        # 查询按钮
        self.searchBtn = gui.Button('计算', width='80%', height=30, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.searchBtn.onclick.do(self.vagueSearchButtonClicked)
        self.vagueSearchPanel.append(self.searchBtn)

        # 结果显示
        self.resultLabel = gui.Label("结果显示在这里", width='80%', height=200, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.vagueSearchPanel.append(self.resultLabel)






        # 页面二
        # 精确计算页面
        self.preciseSearch = gui.Container(width='80%',layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.preciseSearch, '精确计算')
        self.preciseSearchInfo = gui.VBox(width='40%', margin='10px')
        self.preciseSearchPanel = gui.VBox(width='40%', margin='10px')
        self.preciseSearch.append(self.preciseSearchInfo)
        self.preciseSearch.append(self.preciseSearchPanel)

        # 精确计算说明
        self.preciseSearchTitle = gui.Label('关于精确计算', width='80%', style={'font-size': '20px'})
        self.preciseSearchInfo.append(self.preciseSearchTitle)
        self.preciseSearchContent = gui.Label('', width='90%', style={'font-size': '20px'})

        # 选择模型
        self.preciseSearchPanel.append(self.modelSelect)

        # 选择条件
        self.sexSelect = gui.HBox(width='90%', height=20, margin='10px auto')
        self.sexSelectLabel = gui.Label('性别：', width='40%', height=20, margin='10px')
        self.sexSelectDropDown = gui.DropDown.new_from_list(('男', '女'), width='60%', height=20, margin='10px')
        self.selectedSex = ''
        self.sexSelectDropDown.select_by_value(self.selectedSex)
        self.sexSelectDropDown.onchange.do(self.sexSelect_changed)
        self.sexSelect.append(self.sexSelectLabel)
        self.sexSelect.append(self.sexSelectDropDown)
        self.preciseSearchPanel.append(self.sexSelect)

        self.ageInput = gui.HBox(width='90%', height=20, margin='10px auto')
        self.ageInputLabel = gui.Label('年龄：', width='40%', height=20, margin='10px')
        self.ageInputArea = gui.TextInput(width='60%', height=20, margin='10px')
        self.inputedAge = ''
        self.ageInputArea.set_text(self.inputedAge)
        self.ageInputArea.onchange.do(self.ageInputArea_changed)
        self.ageInput.append(self.ageInputLabel)
        self.ageInput.append(self.ageInputArea)
        self.preciseSearchPanel.append(self.ageInput)

        self.eduLevelSelect = gui.HBox(width='90%', height=20, margin='10px auto')
        self.eduLevelSelectLabel = gui.Label('教育程度：', width='40%', height=20, margin='10px')
        self.eduLevelSelectDropDown = gui.DropDown.new_from_list(self.eduLevel, width='60%', height=20, margin='10px')
        self.selectedEduLevel = ''
        self.eduLevelSelectDropDown.select_by_value(self.selectedEduLevel)
        self.eduLevelSelectDropDown.onchange.do(self.eduLevelSelect_changed)
        self.eduLevelSelect.append(self.eduLevelSelectLabel)
        self.eduLevelSelect.append(self.eduLevelSelectDropDown)
        self.preciseSearchPanel.append(self.eduLevelSelect)

        self.jobSelect = gui.HBox(width='90%', height=20, margin='10px auto')
        self.jobSelectLabel = gui.Label('工作：', width='40%', height=20, margin='10px')
        self.jobSelectDropDown = gui.DropDown.new_from_list(self.jobs, width='60%', height=20, margin='10px')
        self.selectedJob = ''
        self.jobSelectDropDown.select_by_value(self.selectedJob)
        self.jobSelectDropDown.onchange.do(self.jobSelect_changed)
        self.jobSelect.append(self.jobSelectLabel)
        self.jobSelect.append(self.jobSelectDropDown)
        self.preciseSearchPanel.append(self.jobSelect)

        self.behaviorSelect = gui.HBox(width='90%', height=20, margin='10px auto')
        self.behaviorSelectLabel = gui.Label('行为：', width='40%', height=20, margin='10px')
        self.behaviorSelectDropDown = gui.DropDown.new_from_list(self.cashOutBehavior, width='60%', height=20, margin='10px')
        self.selectedBehavior = ''
        self.behaviorSelectDropDown.select_by_value(self.selectedBehavior)
        self.behaviorSelectDropDown.onchange.do(self.behaviorSelect_changed)
        self.behaviorSelect.append(self.behaviorSelectLabel)
        self.behaviorSelect.append(self.behaviorSelectDropDown)
        self.preciseSearchPanel.append(self.behaviorSelect)

        self.goalSelect = gui.HBox(width='90%', height=20, margin='10px auto')
        self.goalSelectLabel = gui.Label('目的：', width='40%', height=20, margin='10px')
        self.goalSelectDropDown = gui.DropDown.new_from_list(self.consuGoals, width='60%', height=20, margin='10px')
        self.selectedGoal = ''
        self.goalSelectDropDown.select_by_value(self.selectedGoal)
        self.goalSelectDropDown.onchange.do(self.goalSelect_changed)
        self.goalSelect.append(self.goalSelectLabel)
        self.goalSelect.append(self.goalSelectDropDown)
        self.preciseSearchPanel.append(self.goalSelect)

        self.proofSelect = gui.HBox(width='90%', height=20, margin='10px auto')
        self.proofSelectLabel = gui.Label('证据：', width='40%', height=20, margin='10px')
        self.proofSelectDropDown = gui.DropDown.new_from_list(self.proofs, width='60%', height=20, margin='10px')
        self.selectedProof = ''
        self.proofSelectDropDown.select_by_value(self.selectedProof)
        self.proofSelectDropDown.onchange.do(self.proofSelect_changed)
        self.proofSelect.append(self.proofSelectLabel)
        self.proofSelect.append(self.proofSelectDropDown)
        self.preciseSearchPanel.append(self.proofSelect)



        # 页面三
        # 数据库页面
        self.databaseView = gui.VBox(width='80%', margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.databaseView, '当前数据库')

        # 页面四
        # 介绍页面
        self.aboutUs = gui.VBox(width='80%', margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.aboutUs, '关于我们')

        
        return mainBox

    
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
    

    def vagueSearchButtonClicked(self, widget):
        #   格式： 性别；年龄；教育经历；职业；现金；判决结果；辩护
        #   格式： sex; age; eduLevel; job; cashOut; consuGoal; proof
        if self.currentVagueInput != self.previewVagueInput:
            if len(self.currentVagueInput) < 30:
                self.resultLabel.set_text("警告：信息不足！（请尽可能完整的描述案件）")
            else:
                testVec=[choice(['男', '女']), 36, choice(self.eduLevel), choice(self.jobs), choice(self.cashOutBehavior), choice(self.consuGoals), choice(self.proofs)]
                #testVec=[self.sex.get(), self.old.get(),self.eduLevel.get(), self.job.get(), self.cashOut.get(), self.consuGoal.get(), self.proof.get()]
                predictLabel=self.classify(self.dtree, self.getFeatureLabel(), testVec)
                if predictLabel in self.crime_to_law.keys():
                    self.resultLabel.set_text(predictLabel+"\r\n"+self.crime_to_law[predictLabel])
                else:
                    self.resultLabel.set_text(predictLabel)
                self.previewVagueInput = self.currentVagueInput

    def vagueSearchInput_changed(self, widget, newValue):
        self.currentVagueInput = newValue

    def selectModel_changed(self, widget, value):
        self.selectedModel = value

    def sexSelect_changed(self, widget, value):
        self.selectedSex = value

    def ageInputArea_changed(self, widget, newValue):
        self.inputedAge = newValue

    def eduLevelSelect_changed(self, widget, value):
        self.selectedEduLevel = value

    def jobSelect_changed(self, widget, value):
        self.selectedJob = value

    def behaviorSelect_changed(self, widget, value):
        self.selectedBehavior = value

    def goalSelect_changed(self, widget, value):
        self.selectedGoal = value

    def proofSelect_changed(self, widget, value):
        self.selectedProof = value


if __name__ == '__main__':
    start(MyApp, title="信用卡犯罪预测检索系统", address='0.0.0.0', port=11333, multiple_instance=True)

