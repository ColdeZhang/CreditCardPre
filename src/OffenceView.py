'''
Created on 2020年11月17日

@author: My
'''
from tkinter import StringVar,ttk,PanedWindow,Label,Spinbox,Button

class CrimeView(object):
    def __init__(self, init_window):
        self.init_window=init_window;
        self.panel=PanedWindow(self.init_window.getInitWindow(), orient="vertical",borderwidth=1,relief="raised", width=1124, height=737)
        self.panel.pack(fill="both",expand=1)
        
        self.inputPanl=PanedWindow(self.panel, orient="horizontal",borderwidth=1,relief="raised", width=1123, height=30)
        
        self.sexLabel=Label(self.inputPanl, text="性别")
        self.inputPanl.add(self.sexLabel)
        self.sex=StringVar()
        self.sexComboBox=ttk.Combobox(self.inputPanl, textvariable=self.sex, width=5,state="readonly")
        self.sexComboBox["value"]=("男","女")
        self.sexComboBox.current(0)
        self.inputPanl.add(self.sexComboBox)
        
        self.oldLabel=Label(self.inputPanl, text="年龄")
        self.inputPanl.add(self.oldLabel)
        self.old=StringVar()
        self.oldSpinBox=Spinbox(self.inputPanl, textvariable=self.old, from_=1, to=150, width=5)
        self.inputPanl.add(self.oldSpinBox)
        
        self.eduLevelLabel=Label(self.inputPanl, text="文化程度")
        self.inputPanl.add(self.eduLevelLabel)
        self.eduLevel=StringVar()
        self.eduLevelComboBox=ttk.Combobox(self.inputPanl, textvariable=self.eduLevel, width=10,state="readonly")
        self.eduLevelDataSet=self.init_window.getEduLevels()
        self.eduLevelComboBox["value"]=self.eduLevelDataSet
        self.eduLevelComboBox.current(0)
        self.inputPanl.add(self.eduLevelComboBox)
        
        self.jobLabel=Label(self.inputPanl, text="职业")
        self.inputPanl.add(self.jobLabel)
        self.job=StringVar()
        self.jobComboBox=ttk.Combobox(self.inputPanl, textvariable=self.job, width=15,state="readonly")
        self.jobDataSet=self.init_window.getJobs()
        self.jobComboBox["value"]=self.jobDataSet
        self.jobComboBox.current(0)
        self.inputPanl.add(self.jobComboBox)
        
        self.cashOutLabel=Label(self.inputPanl, text="套现行为")
        self.inputPanl.add(self.cashOutLabel)
        self.cashOut=StringVar()
        self.cashOutComboBox=ttk.Combobox(self.inputPanl, textvariable=self.cashOut, width=25,state="readonly")
        self.cashOutDataSet=self.init_window.getCashOutBehavior()
        self.cashOutComboBox["value"]=self.cashOutDataSet
        self.cashOutComboBox.current(0)
        self.inputPanl.add(self.cashOutComboBox)
        
        self.consuGoalLabel=Label(self.inputPanl, text="目的")
        self.inputPanl.add(self.consuGoalLabel)
        self.consuGoal=StringVar()
        self.consuGoalComboBox=ttk.Combobox(self.inputPanl, textvariable=self.consuGoal, width=35,state="readonly")
        self.consuGoalDataSet=self.init_window.getConsuGoals()
        self.consuGoalComboBox["value"]=self.consuGoalDataSet
        self.consuGoalComboBox.current(0)
        self.inputPanl.add(self.consuGoalComboBox)
        
        self.searchButton=Button(self.inputPanl, text="查询", width=5, command=self.searchButtonClicked)
        self.inputPanl.add(self.searchButton)
        
        self.panel.add(self.inputPanl)
        
        self.inputPanl1=PanedWindow(self.panel, orient="horizontal",borderwidth=1,relief="raised", width=1123, height=30)
        
        self.proofsLabel=Label(self.inputPanl1, text="证据链")
        self.inputPanl1.add(self.proofsLabel)
        self.proof=StringVar()
        self.proofsComboBox=ttk.Combobox(self.inputPanl1, textvariable=self.proof, width=1122,state="readonly")
        self.proofsDataSet=self.init_window.getProofs()
        self.proofsComboBox["value"]=self.proofsDataSet
        self.proofsComboBox.current(0)
        self.inputPanl1.add(self.proofsComboBox)
        
        self.panel.add(self.inputPanl1)
        
        self.label=Label(self.panel, text="",relief="groove",width=1123,height=734)
        self.panel.add(self.label)
        
    def searchButtonClicked(self):
        testVec=[self.sex.get(), self.old.get(),self.eduLevel.get(), self.job.get(), self.cashOut.get(), self.consuGoal.get(), self.proof.get()]
        predictLabel=self.init_window.classify(self.init_window.getDTree(), self.init_window.getFeatureLabel(), testVec)
        if predictLabel in self.init_window.getCrime_to_law().keys():
            self.label.config(text=predictLabel+"\r\n"+self.init_window.getCrime_to_law()[predictLabel])
        else:
            self.label.config(text=predictLabel)
        #print(predictLabel)
        
    def destroy(self):
        self.panel.destroy()
        