# coding: utf-8
from pandas import to_datetime
from numpy import std, nan

class Glucose:  # 要先合并三个血糖csv
    def __init__(self):
        self._initItems()

    # 把csv表格糊进这个dictionary
    def _initItems(self):
        self.glu = []  # 血糖数值
        self.time = []  # 采血时间
        self.timePoint = []  # 时间段
        self.timePointType = []  # 时间段分类

    def append_new_info(self, l):
        self.glu.append(l[0])
        self.time.append(l[1])
        self.timePoint.append(l[2])
        self.timePointType.append(l[3])

class Patient:
    def __init__(self, admitNo_modify):
        self.admitNo_modify = admitNo_modify
        self._initItems()

    def _initItems(self):
        self.name = ""
        self.gender = ""
        self.age = 0
        self.admitNo = 0
        self.deptName = ""

        self.glucose = Glucose()

    def set_basic_info(self, data):
        if (data.empty):
            return
        self.name = data["姓名"].iloc[0].strip()
        self.gender = data["性别"].iloc[0].strip()
        self.age = data["年龄"].iloc[0]
        self.admitNo = data["住院号"].iloc[0]
        self.deptName = data["病区"].iloc[0].strip()

    def set_glucose_info(self, data):
        if (data.empty):
            return
        for i in range(data.shape[0]):
            #t = to_datetime(data["采血时间"].iloc[i])
            new_list = [data["血糖数值"].iloc[i], to_datetime(data["采血时间"].iloc[i]),
                        data["时间段"].iloc[i], data["时间段分类"].iloc[i]]
            self.glucose.append_new_info(new_list)

    def print_info(self):
        print(self.name, self.gender)

class GlucoseSummary:
    def __init__(self):
        self._initItems()

    def _initItems(self):
        self.num = nan
        self.avg = nan
        self.sd = nan
        self.min = nan
        self.max = nan
        self.vhPerc = nan   # >13.9
        self.hPerc = nan    # >10.0
        self.pPerc = nan    # 3.9~10.0
        self.lPerc = nan    # <3.9
        self.vlPerc = nan

    def set_all_glucose(self, Glu, type):
        # type0: all glucose
        # type1: pre-meal glucose
        # type2: post-meal glucose
        # type3: pre-sleep glucose
        # type4: 6:00 glucose

        gluList = []
        for i in range(len(Glu.glu)):
            if (type == 0):
                gluList.append(Glu.glu[i])
            elif (type == Glu.timePointType[i]):
                gluList.append(Glu.glu[i])
            elif (Glu.timePoint[i] == "6点"):
                # type == 4 的情况
                gluList.append(Glu.glu[i])

        self.num = len(gluList)
        if (self.num == 0):
            return
        self.avg = sum(gluList) / len(gluList)
        self.sd = std(gluList) if (self.num >= 2) else nan
        self.min = min(gluList)
        self.max = max(gluList)

        if (type == 0):
            self.vhPerc = sum(i > 13.9 for i in gluList) / self.num
            self.hPerc = sum(i > 10.0 for i in gluList) / self.num
            self.lPerc = sum(i < 3.9 for i in gluList) / self.num
            self.vlPerc = sum(i < 3.0 for i in gluList) / self.num
            self.pPerc = 1 - self.hPerc - self.lPerc

    def print_all_glucose(self):
        # print/append all the itmes
        print("total number:%f\naverage glu:%f\nstd glu:%f\nmin glu:%f\nmax glu:%f\n"
              % (self.num, self.avg, self.sd, self.min, self.max))
        print(">13.9 percent:%f\n>10.0 percent:%f\n3.9~10.0 percent:%f\n"
              "<3.9 percent:%f\n<3.0 percent:%f\n"
              %(self.vhPerc, self.hPerc, self.pPerc, self.lPerc, self.vlPerc))

    def print_part_glucose(self):
        # print/append only num, avg, sd, min, max
        print("total number:%f\naverage glu:%f\nstd glu:%f\nmin glu:%f\nmax glu:%f\n"
              %(self.num, self.avg, self.sd, self.min, self.max))


class PatientSummary:
    def __init__(self):
        self._initItems()

    def _initItems(self):
        self.admitNo = 0
        self.admitNo_modify = ""
        self.name = ""
        self.gender = ""
        self.age = 0
        self.time = ""
        self.containAll = True
        self.allGlucose = GlucoseSummary()
        self.preMealGlucose = GlucoseSummary()
        self.postMealGlucose = GlucoseSummary()
        self.preSleepGlucose = GlucoseSummary()
        self.sixOClockGlucose = GlucoseSummary()

    def set_basic_info_s(self, patient):
        self.admitNo = patient.admitNo
        self.admitNo_modify = patient.admitNo_modify
        self.name = patient.name
        self.gender = patient.gender
        self.age = patient.age
        self.time = patient.glucose.time[0]

    def set_glucose_info_s(self, glucose):
        self.allGlucose.set_all_glucose(glucose, 0)
        self.preMealGlucose.set_all_glucose(glucose, 1)
        self.postMealGlucose.set_all_glucose(glucose, 2)
        self.preSleepGlucose.set_all_glucose(glucose, 3)
        self.sixOClockGlucose.set_all_glucose(glucose, 4)
        self.confirm_contain_all(glucose)

    def confirm_contain_all(self, glucose):
        timePointList = ["6点", "8点30", "10点30", "13点", "16点30", "19点", "21点"]
        for item in timePointList:
            if (item not in glucose.timePoint):
                self.containAll = False
                break

    def print_glucose(self):
        self.allGlucose.print_all_glucose()
        self.preMealGlucose.print_part_glucose()
        self.postMealGlucose.print_part_glucose()
        self.preSleepGlucose.print_part_glucose()