#coding: utf-8
from pandas import to_datetime

key = "采样时间"
value = "数字结果"

class Exam:
    def __init__(self):
        self._initItems()

    #采样时间与上面的项目名称对应，且采样时间在patient里的入院-出院时间之间
    #采样时间作为key，
    def _initItems(self):
        #项目名称
        self.fpgDict = {}   #葡萄糖
        self.hbDict = {}    #糖化血红蛋白
        self.crDict = {}    #肌酐
        self.altDict = {}   #丙氨酸氨基转移酶
        self.astDict = {}   #门冬氨酸氨基转移酶
    
    def set_exam_info(self, data):
        self.set_fpg_info(data)
        self.set_hb_info(data)
        self.set_cr_info(data)
        self.set_alt_info(data)
        self.set_ast_info(data)
        
    def set_fpg_info(self, data):
        fpgData = data.loc[data["项目名称"] == "葡萄糖"]
        fpgKey = fpgData[key]
        fpgValue = fpgData[value]
        for i in range(fpgKey.count()):
            self.fpgDict[fpgKey.iloc[i]] = fpgValue.iloc[i]

    def set_hb_info(self, data):
        hbData = data.loc[data["项目名称"] == "糖化血红蛋白"]
        hbKey = hbData[key]
        hbValue = hbData[value]
        for i in range(hbKey.count()):
            self.hbDict[hbKey.iloc[i]] = hbValue.iloc[i]        

    def set_cr_info(self, data):
        crData = data.loc[data["项目名称"] == "肌酐"]
        crKey = crData[key]
        crValue = crData[value]
        for i in range(crKey.count()):
            self.crDict[crKey.iloc[i]] = crValue.iloc[i]

    def set_alt_info(self, data):
        altData = data.loc[data["项目名称"] == "丙氨酸氨基转移酶"]
        altKey = altData[key]
        altValue = altData[value]
        for i in range(altKey.count()):
            self.altDict[altKey.iloc[i]] = altValue.iloc[i]

    def set_ast_info(self, data):
        astData = data.loc[data["项目名称"] == "门冬氨酸氨基转移酶"]
        astKey = astData[key]
        astValue = astData[value]
        for i in range(astKey.count()):
            self.astDict[astKey.iloc[i]] = astValue.iloc[i]

class Glucose:   #要先合并三个血糖csv
    def __init__(self):
        self._initItems()

    #把csv表格糊进这个dictionary
    def _initItems(self):
        self.glu = []   #csv-血糖数值
        self.time = []  #csv-采血时间
        self.day = []   #csv-采血日期
        self.timePoint = []     #csv-时间点
        self.timePointType = [] #csv-时间点分类
        self.fuce = []  #csv-低血糖复测
        self.fuceTime = []  #csv-低血糖复测时间
    
    def append_new_info(self, l):
        self.glu.append(l[0])
        self.time.append(l[1])
        self.day.append(l[2])
        self.timePoint.append(l[3])
        self.timePointType.append(l[4])
        self.fuce.append(l[5])
        self.fuceTime.append(l[6])

class Patient:
    def __init__(self, admitNo, admitDate):
        self.admitNo = admitNo
        self.admitDate = to_datetime(admitDate)
        self._initItems()

    def _initItems(self):
        self.name = ""
        self.gender = ""
        self.age = 0
        self.dischargeDate = ""
        self.los = 0
        self.deptName = ""
        self.admitDiag = ""
        self.surgeryList = []
        self.exam = Exam()
        self.glucose = Glucose()
    
    def set_basic_info(self, data):
        self.name = data["姓名"].iloc[0].strip()
        self.gender = data["性别"].iloc[0].strip()
        self.age = data["年龄"].iloc[0]
        self.dischargeDate = to_datetime(data["出院时间"].iloc[0])
        self.los = (self.dischargeDate - self.admitDate).days
        self.admitDiag = data["临床诊断"].iloc[0]

        self.exam.set_exam_info(data)

    def set_surgery_info(self, data):
        self.deptName = data["deptname"].iloc[0].strip()
        for i in range(data.shape[0]):
            new_list = [data["admitdiag"].iloc[i], to_datetime(data["applytime"].iloc[i]),
                        data["presurgery"].iloc[i], data["surgeryname"].iloc[i],
                        data["surgerytype"].iloc[i], data["surgerykind"].iloc[i]]
            self.surgeryList.append(new_list)

    def set_glucose_info(self, data):
        for i in range(data.shape[0]):
            t = to_datetime(data["采血时间"].iloc[i])
            if (t >= self.admitDate) and (t <= self.dischargeDate):
                new_list = [data["血糖数值"].iloc[i], to_datetime(data["采血时间"].iloc[i]),
                            data["采血日期"].iloc[i], data["时间点"].iloc[i],
                            data["时间点分类"].iloc[i], data["低血糖复测"].iloc[i],
                            data["低血糖复测时间"].iloc[i]]
                self.glucose.append_new_info(new_list)

    def print_info(self):
        print(self.name, self.gender, self.admitDate, self.dischargeDate)
