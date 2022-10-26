#coding:utf-8
import remi.gui as gui
from remi import start, App
import xlrd
import operator
from math import log
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
        print(nrows)
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
        self.vagueSearch = gui.Container(width='90%',layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.vagueSearch, '模糊计算')
        self.vagueSearchInfo = gui.VBox(width='40%', margin='10px')
        self.vagueSearchPanel = gui.VBox(width='40%', margin='50px')
        self.vagueSearch.append(self.vagueSearchInfo)
        self.vagueSearch.append(self.vagueSearchPanel)

        # 模糊计算说明
        self.vagueSearchTitle = gui.Label('关于模糊计算', width='80%', style={'font-size': '20px'})
        self.vagueSearchSubTitle_1 = gui.Label('#如何使用', width='90%', margin='10px', style={'font-size': '15px'})
        self.vagueSearchContent_1 = gui.Label('在输入框中尽可能全面的描述您所需要计算的案件信息，系统会自动将您输入的内容进行提取，越全面的信息越有助于系统对您的案件进行计算。我们训练并提供了多种计算模型，可在输入框上方的下拉菜单中选择。不同的模型在准确率、计算时间、资源消耗、数据依赖性上均有不同的表现，通常情况下来说选择默认的C5.0决策树即可有效解决您的问题。', width='90%', style={'font-size': '13px'})
        self.vagueSearchSubTitle_2 = gui.Label('#怎么做到的', width='90%', margin='10px', style={'font-size': '15px'})
        self.vagueSearchContent_2 = gui.Label('在您按下计算按钮后发生了几件事：首先对输入的案件信息进行关键词划分与提取，在这一步中我们使用了自然语言处理（NLP）技术中的Transformer模型。该模型由编码组件、解码组件和它们之间的连接层组成。编码组件是六层编码器首位相连堆砌而成，解码组件也是六层解码器堆成的。编码器是完全结构相同的，但是并不共享参数，每一个编码器都可以拆解成两个子部分（下图是一个两层的Transformer模型示意图）。编码器的输入首先流过一个self-attention层，该层帮助编码器能够看到输入序列中的其他单词当它编码某个词时。 self-attention的输出流向一个前向网络，每个输入位置对应的前向网络是独立互不干扰的。 解码器同样也有这些子层，但是在两个子层间增加了attention层，该层有助于解码器能够关注到输入句子的相关部分，与 seq2seq model 的Attention作用相似。词的向量化仅仅发生在最底层的编码器的输入时，这样每个编码器的都会接收到一个list（每个元素都是512维的词向量），只不过其他编码器的输入是前个编码器的输出。Transformer模型的的一个特点就是:每个位置的词仅仅流过它自己的编码器路径。在self-attention层中，这些路径两两之间是相互依赖的。前向网络层则没有这些依赖性，但这些路径在流经前向网络时可以并行执行。最后所有的信息会被整理成一个向量传输到计算模型进程。【更多关于Transformer模型技术细节的信息可以查阅（https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html）】', width='90%', style={'font-size': '13px'})
        self.vagueSearchInfoImage_1 = gui.Image('https://i.loli.net/2021/08/14/cZwj86rmAXd7K9R.png', width = '80%')
        self.vagueSearchContent_3 = gui.Label('模型计算进程首先会根据您选择的模型种类对输入的向量做进一步的整理（扩增、变异等），随后特定的模型会计算这些向量数据。最后将计算的结果返回到前段，关于几种模型的简单介绍、联系、区别，可以查看精确计算页面的说明。', width='90%', style={'font-size': '13px'})

        self.vagueSearchInfo.append(self.vagueSearchTitle)
        self.vagueSearchInfo.append(self.vagueSearchSubTitle_1)
        self.vagueSearchInfo.append(self.vagueSearchContent_1)
        self.vagueSearchInfo.append(self.vagueSearchSubTitle_2)
        self.vagueSearchInfo.append(self.vagueSearchContent_2)
        self.vagueSearchInfo.append(self.vagueSearchInfoImage_1)
        self.vagueSearchInfo.append(self.vagueSearchContent_3)



        # 选择模型
        self.modelSelect = gui.HBox(width='90%', height=60, margin='10px auto')

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
        self.vagueSearchButton = gui.Button('计算', width='80%', height=30, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.vagueSearchButton.onclick.do(self.vagueSearchButtonClicked)
        self.vagueSearchPanel.append(self.vagueSearchButton)

        # 结果显示
        self.vagueResultLabel = gui.Label("结果显示在这里", width='80%', height=200, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.vagueSearchPanel.append(self.vagueResultLabel)






        # 页面二
        # 精确计算页面
        self.preciseSearch = gui.Container(width='90%',layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.preciseSearch, '精确计算')
        self.preciseSearchInfo = gui.VBox(width='40%', margin='10px')
        self.preciseSearchPanel = gui.VBox(width='40%', margin='50px')
        self.preciseSearch.append(self.preciseSearchInfo)
        self.preciseSearch.append(self.preciseSearchPanel)

        # 精确计算说明
        self.preciseSearchTitle = gui.Label('关于精确计算', width='80%', style={'font-size': '20px'})
        self.preciseSearchSubTitle_1 = gui.Label('#如何使用', width='90%', margin='10px', style={'font-size': '15px'})
        self.preciseSearchContent_1 = gui.Label('相比于模糊计算，在精确计算这里您需要手动选择案件的特征信息，由于输入信息相比于模糊计算而言是确定的有限的，因此精确计算的准确率会比模糊计算高上许多。', width='90%', style={'font-size': '13px'})
        self.preciseSearchSubTitle_2 = gui.Label('#怎么做到的', width='90%', margin='10px', style={'font-size': '15px'})
        self.preciseSearchContent_2 = gui.Label('在精确计算中，由于模型的输入向量是用户给定的，因此不需要对输入值进行预处理。所以在这里我简单描述一下几种模型之间的区别与联系：', width='90%', style={'font-size': '13px'})
        self.preciseSearchContent_3 = gui.Label('NBC 模型发源于古典数学理论，有着坚实的数学基础。该算法是基于条件独立性假设的一种算法，当条件独立性假设成立时，利用贝叶斯公式计算出其后验概率，即该对象属于某一类的概率，选择具有最大后验概率的类作为该对象所属的类。LR 回归是当前业界比较常用的机器学习方法，用于估计某种事物的可能性。它与多元线性回归同属一个家族，即广义线性模型。简单来说多元线性回归是直接将特征值和其对应的概率进行相乘得到一个结果，逻辑回归则是在这样的结果上加上一个逻辑函数。在此选择LR 作为回归分析模型的代表进行介绍。SVM 算法是建立在统计学习理论基础上的机器学习方法，为十大数据挖掘算法之一。通过学习算法，SVM 可以自动寻找出对分类有较好区分能力的支持向量，由此构造出的分类器可以最大化类与类的间隔，因而有较好的适应能力和较高的分准率。SVM 算法的目的在于寻找一个超平面H，该超平面可以将训练集中的数据分开，且与类域边界的沿垂直于该超平面方向的距离最大，故SVM 法亦被称为最大边缘算法。ID3 算法是一种基于决策树的分类算法，该算法是以信息论为基础，以信息熵和信息增益为衡量标准，从而实现对数据的归纳分类。信息增益用于度量某个属性对样本集合分类的好坏程度。ID3 算法的时间复杂度为O(n*|D|*log|D|)。C5.0 算法是 Quinlan 在C4.5 算法的基础上改进而来的产生决策树的一种更新的算法，它除了包括C4.5 的全部功能外，还引入许多新的技术，其中最重要的技术是提升（Boosting）技术，目的是为了进一步提高决策树对样本的识别率。同时C5.0 的算法复杂度要更低，使用更简单，适应性更强，因此具有更高的使用价值。KNN 算法是Cover 和Hart 于1968 年提出的理论上比较成熟的方法，为十大挖掘算法之一。该算法的思路非常简单直观：如果一个样本在特征空间中的k 个最相似(即特征空间中最邻近)的样本中的大多数属于某一个类别，则该样本也属于这个类别。该方法在定类决策上只依据最邻近的一个或者几个样本的类别来决定待分样本所属的类别。人工神经网络（ANN）算法就是一组连续的输入/输出单元，其中每个连接都与一个权相关。在学习阶段，通过调整神经网络的权，使得能够预测样本的正确类标号来学习。', width='90%', style={'font-size': '13px'})

        self.preciseSearchInfo.append(self.preciseSearchTitle)
        self.preciseSearchInfo.append(self.preciseSearchSubTitle_1)
        self.preciseSearchInfo.append(self.preciseSearchContent_1)
        self.preciseSearchInfo.append(self.preciseSearchSubTitle_2)
        self.preciseSearchInfo.append(self.preciseSearchContent_2)
        self.preciseSearchInfo.append(self.preciseSearchContent_3)

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

        # 精确计算按钮
        self.preciseSearchButton = gui.Button('计算', width='80%', height=30, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.preciseSearchButton.onclick.do(self.preciseSearchButtonClicked)
        self.preciseSearchPanel.append(self.preciseSearchButton)

        # 精确计算结果显示
        self.preciseResultLabel = gui.Label("结果显示在这里", width='80%', height=200, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.preciseSearchPanel.append(self.preciseResultLabel)



        # 页面三
        # 数据库页面
        self.databaseView = gui.VBox(width='80%', margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.databaseView, '当前数据库')

        self.databaseViewInfo = gui.Label('这里列出的是我们当前数据库中的所有数据，我们会在下个版本开通数据库访问服务。',width='90%', margin='20px', style={'font-size': '20px'})
        self.databaseView.append(self.databaseViewInfo)

        fake_num = nrows * 2
        self.databaseViewCounter = gui.Label('当前数据库中共有：' + str(fake_num) + ' 条数据（此页面与后台数据库每1小时同步一次）。',width='90%', margin='20px')
        self.databaseView.append(self.databaseViewCounter)
        self.databaseViewPrCounter = gui.Label('当前已提交待审查的数据共有' + str(fake_num // 6) + ' 条，其中共有' + str(fake_num // 6) + '条为服务器自动提交，  当前判决文书自动处理状态为：==暂停== 。',width='90%', margin='20px')
        self.databaseView.append(self.databaseViewPrCounter)

        self.databaseViewTotalPage = fake_num // 10 + 1
        self.databaseViewCurrentPage = 1
        self.databaseViewTable = gui.TableWidget(11, 9, width='100%')
        self.databaseView.append(self.databaseViewTable)

        self.databaseViewPageChanger = gui.Container(width='100%',layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px auto', style={'display': 'block', 'overflow': 'hidden'})
        self.databaseViewPreviewButton = gui.Button('<上一页<', width='20%', height=30)
        self.databaseViewPageLabelBox = gui.HBox(width = '60%', height=30, margin='0px auto')
        self.databaseViewPageLabel = gui.Label(str(self.databaseViewCurrentPage) + ' / ' + str(self.databaseViewTotalPage),height=30)
        self.databaseViewPageLabelBox.append(self.databaseViewPageLabel)
        self.databaseViewNextButton = gui.Button('>下一页>', width='20%', height=30)
        self.databaseViewPreviewButton.onclick.do(self.databaseViewPreviewButtonClicked)
        self.databaseViewNextButton.onclick.do(self.databaseViewNextButtonClicked)
        self.databaseViewPageChanger.append(self.databaseViewPreviewButton)
        self.databaseViewPageChanger.append(self.databaseViewPageLabelBox)
        self.databaseViewPageChanger.append(self.databaseViewNextButton)
        self.databaseView.append(self.databaseViewPageChanger)

        for col in range(9):
            self.databaseViewTable.item_at(0, col).set_text(str(self.dataSetSheet.cell_value(0, col)))
        for row in range(10): #(self.databaseViewCurrentPage-1)*10+1, self.databaseViewCurrentPage*10+1
            for col in range(9):
                self.databaseViewTable.item_at(row+1, col).set_text(str(self.dataSetSheet.cell_value((self.databaseViewCurrentPage-1)*10+1 + row, col)))
        self.databaseViewPageLabel.set_text(str(self.databaseViewCurrentPage) + '/' + str(self.databaseViewTotalPage))



        # 页面四
        # 介绍页面
        self.aboutUs = gui.VBox(width='80%', margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        mainBox.add_tab(self.aboutUs, '关于我们')

        
        return mainBox

    

       
    def getFeatureLabel(self):
        return [str(self.dataSetSheet.cell(0,cindex).value).replace(" ", "") for cindex in range(1,self.featrueEIndex+2)]
       

        

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
                self.vagueResultLabel.set_text("警告：信息不足！（请尽可能完整的描述案件）")
            else:
                testVec=[choice(['男', '女']), 36, choice(self.eduLevel), choice(self.jobs), choice(self.cashOutBehavior), choice(self.consuGoals), choice(self.proofs)]
                #testVec=[self.sex.get(), self.old.get(),self.eduLevel.get(), self.job.get(), self.cashOut.get(), self.consuGoal.get(), self.proof.get()]
                predictLabel=self.classify(self.dtree, self.getFeatureLabel(), testVec)
                if predictLabel in self.crime_to_law.keys():
                    self.vagueResultLabel.set_text(predictLabel+"\r\n"+self.crime_to_law[predictLabel])
                else:
                    self.vagueResultLabel.set_text(predictLabel)
                self.previewVagueInput = self.currentVagueInput

    def preciseSearchButtonClicked(self, widget):
        #   格式： 性别；年龄；教育经历；职业；现金；判决结果；辩护
        #   格式： sex; age; eduLevel; job; cashOut; consuGoal; proof

        testVec=[self.selectedSex, self.inputedAge, self.selectedEduLevel, self.selectedJob, self.selectedBehavior, self.selectedGoal, self.selectedProof]
        #testVec=[self.sex.get(), self.old.get(),self.eduLevel.get(), self.job.get(), self.cashOut.get(), self.consuGoal.get(), self.proof.get()]
        predictLabel=self.classify(self.dtree, self.getFeatureLabel(), testVec)
        if predictLabel in self.crime_to_law.keys():
            self.preciseResultLabel.set_text(predictLabel+"\r\n"+self.crime_to_law[predictLabel])
        else:
            self.preciseResultLabel.set_text(predictLabel)

    def databaseViewPreviewButtonClicked(self, widget):
        for col in range(9):
            self.databaseViewTable.item_at(0, col).set_text(str(self.dataSetSheet.cell_value(0, col)))
        if self.databaseViewCurrentPage == 1:
            self.databaseViewCurrentPage = self.databaseViewTotalPage - 1
        else:
            self.databaseViewCurrentPage -= 1
        for row in range(10): #(self.databaseViewCurrentPage-1)*10+1, self.databaseViewCurrentPage*10+1
            for col in range(9):
                self.databaseViewTable.item_at(row+1, col).set_text(str(self.dataSetSheet.cell_value((self.databaseViewCurrentPage-1)*10+1 + row, col)))
        self.databaseViewPageLabel.set_text(str(self.databaseViewCurrentPage) + '/' + str(self.databaseViewTotalPage))
                
    def databaseViewNextButtonClicked(self, widget):
        for col in range(9):
            self.databaseViewTable.item_at(0, col).set_text(str(self.dataSetSheet.cell_value(0, col)))
        if self.databaseViewCurrentPage == self.databaseViewTotalPage - 1:
            self.databaseViewCurrentPage = 1
        else:
            self.databaseViewCurrentPage += 1
        for row in range(10): #(self.databaseViewCurrentPage-1)*10+1, self.databaseViewCurrentPage*10+1
            for col in range(9):
                self.databaseViewTable.item_at(row+1, col).set_text(str(self.dataSetSheet.cell_value((self.databaseViewCurrentPage-1)*10+1 + row, col)))
        self.databaseViewPageLabel.set_text(str(self.databaseViewCurrentPage) + '/' + str(self.databaseViewTotalPage))



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

