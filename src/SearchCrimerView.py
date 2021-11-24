'''
Created on 2020年11月17日

@author: My
'''
from tkinter import END,StringVar,ttk,PanedWindow,Label,Scrollbar,Listbox

class CrimerView(object):
    def __init__(self, init_window):
        self.init_window=init_window
        self.panel=PanedWindow(self.init_window.getInitWindow(), orient="vertical",borderwidth=1,relief="raised", width=1124, height=737)
        self.panel.pack(fill="both",expand=1)
        
        self.inputPanl=PanedWindow(self.panel, orient="horizontal",borderwidth=1,relief="raised", width=1123, height=30)
        
        self.crimeLabel=Label(self.inputPanl, text="罪名")
        self.inputPanl.add(self.crimeLabel)
        self.crime=StringVar()
        self.crimeComboBox=ttk.Combobox(self.inputPanl, textvariable=self.crime, width=80,state="readonly")
        self.crimeDataSet=self.init_window.getCrimes()
        self.crimeComboBox["value"]=self.crimeDataSet
        self.crimeComboBox.current(0)
        self.crimeComboBox.bind("<<ComboboxSelected>>",self.crimeComboBoxSelectValueChanged)
        self.inputPanl.add(self.crimeComboBox)
        
        self.featureItem=StringVar()
        self.featureItemComboBox=ttk.Combobox(self.inputPanl, textvariable=self.featureItem, width=50,state="readonly")
        self.featureItemDataSet=self.init_window.getFeatureLabel()[:-1]
        self.featureItemComboBox["value"]=self.featureItemDataSet
        self.featureItemComboBox.current(0)
        self.featureItemComboBox.bind("<<ComboboxSelected>>",self.featureItemComboBoxSelectValueChanged)
        self.inputPanl.add(self.featureItemComboBox)
        
        self.panel.add(self.inputPanl)
        self.gridView=PanedWindow(self.panel, orient="vertical",borderwidth=1,relief="raised", width=1123, height=706)
        self.scrollBar=Scrollbar(self.gridView)
        self.scrollBar.pack(side="right", fill="y")
        self.listBox=Listbox(self.panel, relief="groove", width=1123, height=705, yscrollcommand=self.scrollBar.set)
        self.gridView.add(self.listBox)
        self.panel.add(self.gridView)
        
        self.records=["男性:"+str(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if "男" in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)+"%","女性:"+str(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if "女" in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)+"%"]
        for record in self.records:
            self.listBox.insert(END, record)
     
    def crimeComboBoxSelectValueChanged(self, *args):
        self.listBox.delete(0,END) 
        if "性别"==self.featureItem.get():
            self.getSexData()
        elif "文化水平"==self.featureItem.get():
            self.getEduLevelData()
            
        for record in self.records:
            self.listBox.insert(END, record)
                   
    def featureItemComboBoxSelectValueChanged(self, *args):
        self.listBox.delete(0,END) 
        if "性别"==self.featureItem.get():
            self.getSexData()
        elif "文化水平"==self.featureItem.get():
            self.getEduLevelData()
        elif "年龄"==self.featureItem.get():
            self.getOldsData()
        elif "职业"==self.featureItem.get():
            self.getJobsData()
        elif "套现行为"==self.featureItem.get():
            self.getCashOutBehaviorData()
        elif "目的"==self.featureItem.get():
            self.getConsuGoalsData()
        elif "证据链"==self.featureItem.get():
            self.getProofsData()
                
        for record in self.records:
            self.listBox.insert(END, record)
    
    def getSexData(self):
        self.records=[
                      "男性:"+str( ("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if "男" in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100))) +"%",
                      "女性:"+str(("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if "女" in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)))+"%"
                      ]
    
    def getEduLevelData(self):
        self.records=[]
        for edu in self.init_window.getEduLevels():
            self.records.append(edu+":"+
            str( ("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if edu in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)))+"%")            
    
    def getOldsData(self):
        self.records=[]
        for old in self.init_window.getOlds():
            self.records.append(old+"岁:"+str( ("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if old in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)))+"%")
    
    def getJobsData(self):
        self.records=[]
        for job in self.init_window.getJobs():
            self.records.append(job+":"+str( ("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if job in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)))+"%")
       
    def getCashOutBehaviorData(self):
        self.records=[]
        for behavior in self.init_window.getCashOutBehavior():
            self.records.append(behavior+":"+str( ("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if behavior in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)))+"%")
            
    def getConsuGoalsData(self):
        self.records=[]
        for goal in self.init_window.getConsuGoals():
            self.records.append(goal+":"+str( ("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if goal in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)))+"%")
            
    def getProofsData(self):
        self.records=[]
        for proof in self.init_window.getProofs():
            self.records.append(proof+":"+str( ("%.2f"%(len([item for item in self.init_window.getCrime_to_records()[self.crime.get()] if proof in  item])/len(self.init_window.getCrime_to_records()[self.crime.get()])*100)))+"%")
                      
    def destroy(self):
        self.panel.destroy()