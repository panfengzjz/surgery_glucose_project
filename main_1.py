# coding: utf-8
import pandas as pd
from patientCLass_1 import Patient
from patientCLass_1 import PatientSummary

fileName = "基线2015-2017内分泌所有住院血糖.xlsx"
df = pd.read_excel(fileName)
dayNum = 5

def load_patient_list(anList):
    patientList = []
    for an in anList:
        pData = df.loc[df["admitNo_modify"] == an]
        if (pData.empty):
            continue
        patientList.append(Patient(an))
    return patientList

def load_patient_day_list(patientList):
    patientDayList = []
    for p in patientList:
        pData = df.loc[df["admitNo_modify"] == p.admitNo_modify]
        if (pData.empty):
            continue
        pDayxList = []
        admitDay = 0
        curDay = admitDay
        for i in range(pData.shape[0]):
            preDay = curDay
            curDay = pd.to_datetime(pData["采血日期"].iloc[i])
            if (curDay != preDay):
                pDayxList.append(curDay)
                if len(pDayxList) >= dayNum:
                    break
        patientDayList.append(pDayxList)
    return patientDayList

def set_exam_item(patientList):
    for p in patientList:
        pId = p.admitNo_modify
        pData = df.loc[(df["admitNo_modify"] == pId)]
        if (pData.empty):
            continue
        p.set_basic_info(pData)
        p.set_glucose_info(pData)

def set_exam_item_based_on_day(patientList, dayList):
    patientDayList = []
    i = 0
    for p in patientList:
        onePatientList = []
        day = dayList[i]
        i = i+1
        for d in day:
            pId = p.admitNo_modify
            pData = df.loc[(df["admitNo_modify"] == pId)
                           & (pd.to_datetime(df["采血日期"]) == d)]
            if (pData.empty):
                return # this patient does not have further info to process
            pDay = Patient(pId)
            pDay.set_basic_info(pData)
            pDay.set_glucose_info(pData)
            onePatientList.append(pDay)
        patientDayList.append(onePatientList)
    return patientDayList
        #
        # pData = df.loc[(df["admitNo_modify"] == pId)]
        # if (pData.empty):
        #     continue
        # dxData = pd.DataFrame(columns=pData.columns)
        # admitDate = pd.to_datetime(pData["采血时间"].iloc[0])
        # for i in range(pData.shape[0]):
        #     curDate = pd.to_datetime(pData["采血时间"].iloc[i])
        #     if ((curDate - admitDate).days == dayDist):
        #         tmpData = pData.iloc[[i]] # 要保持取出数据依旧是 dataframe，而不是 series，需要用两个[]
        #         dxData = pd.concat([dxData, tmpData])
        #     if ((curDate - admitDate).days > dayDist):
        #         break
        # if (dxData.empty):
        #     continue
        # p.set_basic_info(dxData)
        # p.set_glucose_info(dxData)

def set_glucose_item(patientList):
    psList = []
    for p in patientList:
        ps = PatientSummary()
        ps.set_basic_info_s(p)
        ps.set_glucose_info_s(p.glucose)
        psList.append(ps)
    return psList

def set_glucose_item_on_day(patientDayList):
    psDayList = []
    for pL in patientDayList:
        psList = []
        for p in pL:
            ps = PatientSummary()
            ps.set_basic_info_s(p)
            ps.set_glucose_info_s(p.glucose)
            psList.append(ps)
        psDayList.append(psList)
    return psDayList

def print_patient_summary(psList):
    for ps in psList:
        ps.print_glucose()

def print_to_excel(psList, psDayList):
    dfColumns = ["住院号", "admitNo_modify", "姓名", "年龄", "性别", "采血时间", "是否七个时刻都有血糖监测",
                 "所有血糖总条数", "所有血糖均值", "所有血糖标准差", "所有血糖最小值", "所有血糖最大值",
                 ">13.9比例", ">10比例", "3.9~10比例", "<3.9比例", "<3.0比例",
                 "餐前血糖总条数", "餐前血糖均值", "餐前血糖标准差", "餐前血糖最小值", "餐前血糖最大值",
                 "餐后血糖总条数", "餐后血糖均值", "餐后血糖标准差", "餐后血糖最小值", "餐后血糖最大值",
                 "睡前血糖总条数", "睡前血糖均值", "睡前血糖标准差", "睡前血糖最小值", "睡前血糖最大值",
                 "6点血糖总条数", "6点血糖均值", "6点血糖标准差", "6点血糖最小值", "6点血糖最大值",
                 "第一天所有血糖总条数", "第一天所有血糖均值", "第一天所有血糖标准差", "第一天所有血糖最小值", "第一天所有血糖最大值",
                 "第一天餐前血糖总条数", "第一天餐前血糖均值", "第一天餐前血糖标准差", "第一天餐前血糖最小值", "第一天餐前血糖最大值",
                 "第一天餐后血糖总条数", "第一天餐后血糖均值", "第一天餐后血糖标准差", "第一天餐后血糖最小值", "第一天餐后血糖最大值",
                 "第一天睡前血糖总条数", "第一天睡前血糖均值", "第一天睡前血糖标准差", "第一天睡前血糖最小值", "第一天睡前血糖最大值",
                 "第一天6点血糖总条数", "第一天6点血糖均值", "第一天6点血糖标准差", "第一天6点血糖最小值", "第一天6点血糖最大值",
                 "第二天所有血糖总条数", "第二天所有血糖均值", "第二天所有血糖标准差", "第二天所有血糖最小值", "第二天所有血糖最大值",
                 "第二天餐前血糖总条数", "第二天餐前血糖均值", "第二天餐前血糖标准差", "第二天餐前血糖最小值", "第二天餐前血糖最大值",
                 "第二天餐后血糖总条数", "第二天餐后血糖均值", "第二天餐后血糖标准差", "第二天餐后血糖最小值", "第二天餐后血糖最大值",
                 "第二天睡前血糖总条数", "第二天睡前血糖均值", "第二天睡前血糖标准差", "第二天睡前血糖最小值", "第二天睡前血糖最大值",
                 "第二天6点血糖总条数", "第二天6点血糖均值", "第二天6点血糖标准差", "第二天6点血糖最小值", "第二天6点血糖最大值",
                 "第三天所有血糖总条数", "第三天所有血糖均值", "第三天所有血糖标准差", "第三天所有血糖最小值", "第三天所有血糖最大值",
                 "第三天餐前血糖总条数", "第三天餐前血糖均值", "第三天餐前血糖标准差", "第三天餐前血糖最小值", "第三天餐前血糖最大值",
                 "第三天餐后血糖总条数", "第三天餐后血糖均值", "第三天餐后血糖标准差", "第三天餐后血糖最小值", "第三天餐后血糖最大值",
                 "第三天睡前血糖总条数", "第三天睡前血糖均值", "第三天睡前血糖标准差", "第三天睡前血糖最小值", "第三天睡前血糖最大值",
                 "第三天6点血糖总条数", "第三天6点血糖均值", "第三天6点血糖标准差", "第三天6点血糖最小值", "第三天6点血糖最大值",
                 "第四天所有血糖总条数", "第四天所有血糖均值", "第四天所有血糖标准差", "第四天所有血糖最小值", "第四天所有血糖最大值",
                 "第四天餐前血糖总条数", "第四天餐前血糖均值", "第四天餐前血糖标准差", "第四天餐前血糖最小值", "第四天餐前血糖最大值",
                 "第四天餐后血糖总条数", "第四天餐后血糖均值", "第四天餐后血糖标准差", "第四天餐后血糖最小值", "第四天餐后血糖最大值",
                 "第四天睡前血糖总条数", "第四天睡前血糖均值", "第四天睡前血糖标准差", "第四天睡前血糖最小值", "第四天睡前血糖最大值",
                 "第四天6点血糖总条数", "第四天6点血糖均值", "第四天6点血糖标准差", "第四天6点血糖最小值", "第四天6点血糖最大值",
                 "第五天所有血糖总条数", "第五天所有血糖均值", "第五天所有血糖标准差", "第五天所有血糖最小值", "第五天所有血糖最大值",
                 "第五天餐前血糖总条数", "第五天餐前血糖均值", "第五天餐前血糖标准差", "第五天餐前血糖最小值", "第五天餐前血糖最大值",
                 "第五天餐后血糖总条数", "第五天餐后血糖均值", "第五天餐后血糖标准差", "第五天餐后血糖最小值", "第五天餐后血糖最大值",
                 "第五天睡前血糖总条数", "第五天睡前血糖均值", "第五天睡前血糖标准差", "第五天睡前血糖最小值", "第五天睡前血糖最大值",
                 "第五天6点血糖总条数", "第五天6点血糖均值", "第五天6点血糖标准差", "第五天6点血糖最小值", "第五天6点血糖最大值",
                 ]
    pData = pd.DataFrame(columns=dfColumns)
    for i in range(len(psList)):
        ps = psList[i]
        ps_day1 = psDayList[i][0] if len(psDayList[i]) >= 1 else 0
        ps_day2 = psDayList[i][1] if len(psDayList[i]) >= 2 else 0
        ps_day3 = psDayList[i][2] if len(psDayList[i]) >= 3 else 0
        ps_day4 = psDayList[i][3] if len(psDayList[i]) >= 4 else 0
        ps_day5 = psDayList[i][4] if len(psDayList[i]) >= 5 else 0

        tmpData = pd.DataFrame(columns=dfColumns)
        tmpData["住院号"] = [ps.admitNo]
        tmpData["admitNo_modify"] = ps.admitNo_modify
        tmpData["姓名"] = ps.name
        tmpData["年龄"] = ps.age
        tmpData["性别"] = ps.gender
        tmpData["采血时间"] = ps.time
        tmpData["是否七个时刻都有血糖监测"] = ps.containAll

        tmpData["所有血糖总条数"] = ps.allGlucose.num
        tmpData["所有血糖均值"] = ps.allGlucose.avg
        tmpData["所有血糖标准差"] = ps.allGlucose.sd
        tmpData["所有血糖最小值"] = ps.allGlucose.min
        tmpData["所有血糖最大值"] = ps.allGlucose.max
        tmpData[">13.9比例"] = ps.allGlucose.vhPerc
        tmpData[">10比例"] = ps.allGlucose.hPerc
        tmpData["3.9~10比例"] = ps.allGlucose.pPerc
        tmpData["<3.9比例"] = ps.allGlucose.lPerc
        tmpData["<3.0比例"] = ps.allGlucose.vlPerc

        tmpData["餐前血糖总条数"] = ps.preMealGlucose.num
        tmpData["餐前血糖均值"] = ps.preMealGlucose.avg
        tmpData["餐前血糖标准差"] = ps.preMealGlucose.sd
        tmpData["餐前血糖最小值"] = ps.preMealGlucose.min
        tmpData["餐前血糖最大值"] = ps.preMealGlucose.max

        tmpData["餐后血糖总条数"] = ps.postMealGlucose.num
        tmpData["餐后血糖均值"] = ps.postMealGlucose.avg
        tmpData["餐后血糖标准差"] = ps.postMealGlucose.sd
        tmpData["餐后血糖最小值"] = ps.postMealGlucose.min
        tmpData["餐后血糖最大值"] = ps.postMealGlucose.max

        tmpData["睡前血糖总条数"] = ps.preSleepGlucose.num
        tmpData["睡前血糖均值"] = ps.preSleepGlucose.avg
        tmpData["睡前血糖标准差"] = ps.preSleepGlucose.sd
        tmpData["睡前血糖最小值"] = ps.preSleepGlucose.min
        tmpData["睡前血糖最大值"] = ps.preSleepGlucose.max

        tmpData["6点血糖总条数"] = ps.sixOClockGlucose.num
        tmpData["6点血糖均值"] = ps.sixOClockGlucose.avg
        tmpData["6点血糖标准差"] = ps.sixOClockGlucose.sd
        tmpData["6点血糖最小值"] = ps.sixOClockGlucose.min
        tmpData["6点血糖最大值"] = ps.sixOClockGlucose.max

        if (not ps_day1):
            continue
        tmpData["第一天所有血糖总条数"] = ps_day1.allGlucose.num
        tmpData["第一天所有血糖均值"] = ps_day1.allGlucose.avg
        tmpData["第一天所有血糖标准差"] = ps_day1.allGlucose.sd
        tmpData["第一天所有血糖最小值"] = ps_day1.allGlucose.min
        tmpData["第一天所有血糖最大值"] = ps_day1.allGlucose.max

        tmpData["第一天餐前血糖总条数"] = ps_day1.preMealGlucose.num
        tmpData["第一天餐前血糖均值"] = ps_day1.preMealGlucose.avg
        tmpData["第一天餐前血糖标准差"] = ps_day1.preMealGlucose.sd
        tmpData["第一天餐前血糖最小值"] = ps_day1.preMealGlucose.min
        tmpData["第一天餐前血糖最大值"] = ps_day1.preMealGlucose.max

        tmpData["第一天餐后血糖总条数"] = ps_day1.postMealGlucose.num
        tmpData["第一天餐后血糖均值"] = ps_day1.postMealGlucose.avg
        tmpData["第一天餐后血糖标准差"] = ps_day1.postMealGlucose.sd
        tmpData["第一天餐后血糖最小值"] = ps_day1.postMealGlucose.min
        tmpData["第一天餐后血糖最大值"] = ps_day1.postMealGlucose.max

        tmpData["第一天睡前血糖总条数"] = ps_day1.preSleepGlucose.num
        tmpData["第一天睡前血糖均值"] = ps_day1.preSleepGlucose.avg
        tmpData["第一天睡前血糖标准差"] = ps_day1.preSleepGlucose.sd
        tmpData["第一天睡前血糖最小值"] = ps_day1.preSleepGlucose.min
        tmpData["第一天睡前血糖最大值"] = ps_day1.preSleepGlucose.max

        tmpData["第一天6点血糖总条数"] = ps_day1.sixOClockGlucose.num
        tmpData["第一天6点血糖均值"] = ps_day1.sixOClockGlucose.avg
        tmpData["第一天6点血糖标准差"] = ps_day1.sixOClockGlucose.sd
        tmpData["第一天6点血糖最小值"] = ps_day1.sixOClockGlucose.min
        tmpData["第一天6点血糖最大值"] = ps_day1.sixOClockGlucose.max

        if (not ps_day2):
            continue
        tmpData["第二天所有血糖总条数"] = ps_day2.allGlucose.num
        tmpData["第二天所有血糖均值"] = ps_day2.allGlucose.avg
        tmpData["第二天所有血糖标准差"] = ps_day2.allGlucose.sd
        tmpData["第二天所有血糖最小值"] = ps_day2.allGlucose.min
        tmpData["第二天所有血糖最大值"] = ps_day2.allGlucose.max

        tmpData["第二天餐前血糖总条数"] = ps_day2.preMealGlucose.num
        tmpData["第二天餐前血糖均值"] = ps_day2.preMealGlucose.avg
        tmpData["第二天餐前血糖标准差"] = ps_day2.preMealGlucose.sd
        tmpData["第二天餐前血糖最小值"] = ps_day2.preMealGlucose.min
        tmpData["第二天餐前血糖最大值"] = ps_day2.preMealGlucose.max

        tmpData["第二天餐后血糖总条数"] = ps_day2.postMealGlucose.num
        tmpData["第二天餐后血糖均值"] = ps_day2.postMealGlucose.avg
        tmpData["第二天餐后血糖标准差"] = ps_day2.postMealGlucose.sd
        tmpData["第二天餐后血糖最小值"] = ps_day2.postMealGlucose.min
        tmpData["第二天餐后血糖最大值"] = ps_day2.postMealGlucose.max

        tmpData["第二天睡前血糖总条数"] = ps_day2.preSleepGlucose.num
        tmpData["第二天睡前血糖均值"] = ps_day2.preSleepGlucose.avg
        tmpData["第二天睡前血糖标准差"] = ps_day2.preSleepGlucose.sd
        tmpData["第二天睡前血糖最小值"] = ps_day2.preSleepGlucose.min
        tmpData["第二天睡前血糖最大值"] = ps_day2.preSleepGlucose.max

        tmpData["第二天6点血糖总条数"] = ps_day2.sixOClockGlucose.num
        tmpData["第二天6点血糖均值"] = ps_day2.sixOClockGlucose.avg
        tmpData["第二天6点血糖标准差"] = ps_day2.sixOClockGlucose.sd
        tmpData["第二天6点血糖最小值"] = ps_day2.sixOClockGlucose.min
        tmpData["第二天6点血糖最大值"] = ps_day2.sixOClockGlucose.max

        if (not ps_day3):
            continue
        tmpData["第三天所有血糖总条数"] = ps_day3.allGlucose.num
        tmpData["第三天所有血糖均值"] = ps_day3.allGlucose.avg
        tmpData["第三天所有血糖标准差"] = ps_day3.allGlucose.sd
        tmpData["第三天所有血糖最小值"] = ps_day3.allGlucose.min
        tmpData["第三天所有血糖最大值"] = ps_day3.allGlucose.max

        tmpData["第三天餐前血糖总条数"] = ps_day3.preMealGlucose.num
        tmpData["第三天餐前血糖均值"] = ps_day3.preMealGlucose.avg
        tmpData["第三天餐前血糖标准差"] = ps_day3.preMealGlucose.sd
        tmpData["第三天餐前血糖最小值"] = ps_day3.preMealGlucose.min
        tmpData["第三天餐前血糖最大值"] = ps_day3.preMealGlucose.max

        tmpData["第三天餐后血糖总条数"] = ps_day3.postMealGlucose.num
        tmpData["第三天餐后血糖均值"] = ps_day3.postMealGlucose.avg
        tmpData["第三天餐后血糖标准差"] = ps_day3.postMealGlucose.sd
        tmpData["第三天餐后血糖最小值"] = ps_day3.postMealGlucose.min
        tmpData["第三天餐后血糖最大值"] = ps_day3.postMealGlucose.max

        tmpData["第三天睡前血糖总条数"] = ps_day3.preSleepGlucose.num
        tmpData["第三天睡前血糖均值"] = ps_day3.preSleepGlucose.avg
        tmpData["第三天睡前血糖标准差"] = ps_day3.preSleepGlucose.sd
        tmpData["第三天睡前血糖最小值"] = ps_day3.preSleepGlucose.min
        tmpData["第三天睡前血糖最大值"] = ps_day3.preSleepGlucose.max

        tmpData["第三天6点血糖总条数"] = ps_day3.sixOClockGlucose.num
        tmpData["第三天6点血糖均值"] = ps_day3.sixOClockGlucose.avg
        tmpData["第三天6点血糖标准差"] = ps_day3.sixOClockGlucose.sd
        tmpData["第三天6点血糖最小值"] = ps_day3.sixOClockGlucose.min
        tmpData["第三天6点血糖最大值"] = ps_day3.sixOClockGlucose.max

        if (not ps_day4):
            continue
        tmpData["第四天所有血糖总条数"] = ps_day4.allGlucose.num
        tmpData["第四天所有血糖均值"] = ps_day4.allGlucose.avg
        tmpData["第四天所有血糖标准差"] = ps_day4.allGlucose.sd
        tmpData["第四天所有血糖最小值"] = ps_day4.allGlucose.min
        tmpData["第四天所有血糖最大值"] = ps_day4.allGlucose.max

        tmpData["第四天餐前血糖总条数"] = ps_day4.preMealGlucose.num
        tmpData["第四天餐前血糖均值"] = ps_day4.preMealGlucose.avg
        tmpData["第四天餐前血糖标准差"] = ps_day4.preMealGlucose.sd
        tmpData["第四天餐前血糖最小值"] = ps_day4.preMealGlucose.min
        tmpData["第四天餐前血糖最大值"] = ps_day4.preMealGlucose.max

        tmpData["第四天餐后血糖总条数"] = ps_day4.postMealGlucose.num
        tmpData["第四天餐后血糖均值"] = ps_day4.postMealGlucose.avg
        tmpData["第四天餐后血糖标准差"] = ps_day4.postMealGlucose.sd
        tmpData["第四天餐后血糖最小值"] = ps_day4.postMealGlucose.min
        tmpData["第四天餐后血糖最大值"] = ps_day4.postMealGlucose.max

        tmpData["第四天睡前血糖总条数"] = ps_day4.preSleepGlucose.num
        tmpData["第四天睡前血糖均值"] = ps_day4.preSleepGlucose.avg
        tmpData["第四天睡前血糖标准差"] = ps_day4.preSleepGlucose.sd
        tmpData["第四天睡前血糖最小值"] = ps_day4.preSleepGlucose.min
        tmpData["第四天睡前血糖最大值"] = ps_day4.preSleepGlucose.max

        tmpData["第四天6点血糖总条数"] = ps_day4.sixOClockGlucose.num
        tmpData["第四天6点血糖均值"] = ps_day4.sixOClockGlucose.avg
        tmpData["第四天6点血糖标准差"] = ps_day4.sixOClockGlucose.sd
        tmpData["第四天6点血糖最小值"] = ps_day4.sixOClockGlucose.min
        tmpData["第四天6点血糖最大值"] = ps_day4.sixOClockGlucose.max

        if (not ps_day5):
            continue
        tmpData["第五天所有血糖总条数"] = ps_day5.allGlucose.num
        tmpData["第五天所有血糖均值"] = ps_day5.allGlucose.avg
        tmpData["第五天所有血糖标准差"] = ps_day5.allGlucose.sd
        tmpData["第五天所有血糖最小值"] = ps_day5.allGlucose.min
        tmpData["第五天所有血糖最大值"] = ps_day5.allGlucose.max

        tmpData["第五天餐前血糖总条数"] = ps_day5.preMealGlucose.num
        tmpData["第五天餐前血糖均值"] = ps_day5.preMealGlucose.avg
        tmpData["第五天餐前血糖标准差"] = ps_day5.preMealGlucose.sd
        tmpData["第五天餐前血糖最小值"] = ps_day5.preMealGlucose.min
        tmpData["第五天餐前血糖最大值"] = ps_day5.preMealGlucose.max

        tmpData["第五天餐后血糖总条数"] = ps_day5.postMealGlucose.num
        tmpData["第五天餐后血糖均值"] = ps_day5.postMealGlucose.avg
        tmpData["第五天餐后血糖标准差"] = ps_day5.postMealGlucose.sd
        tmpData["第五天餐后血糖最小值"] = ps_day5.postMealGlucose.min
        tmpData["第五天餐后血糖最大值"] = ps_day5.postMealGlucose.max

        tmpData["第五天睡前血糖总条数"] = ps_day5.preSleepGlucose.num
        tmpData["第五天睡前血糖均值"] = ps_day5.preSleepGlucose.avg
        tmpData["第五天睡前血糖标准差"] = ps_day5.preSleepGlucose.sd
        tmpData["第五天睡前血糖最小值"] = ps_day5.preSleepGlucose.min
        tmpData["第五天睡前血糖最大值"] = ps_day5.preSleepGlucose.max

        tmpData["第五天6点血糖总条数"] = ps_day5.sixOClockGlucose.num
        tmpData["第五天6点血糖均值"] = ps_day5.sixOClockGlucose.avg
        tmpData["第五天6点血糖标准差"] = ps_day5.sixOClockGlucose.sd
        tmpData["第五天6点血糖最小值"] = ps_day5.sixOClockGlucose.min
        tmpData["第五天6点血糖最大值"] = ps_day5.sixOClockGlucose.max

        pData = pd.concat([pData, tmpData])
    pData.to_excel("result.xlsx")

def update_admit_no():
    global df
    df["admitNo_modify"] = ""
    df["采血日期"] = ""
    pData = pd.DataFrame(columns=df.columns)
    admitList = set(df["住院号"])
    for ad in admitList:
        tmpData = df.loc[(df["住院号"] == ad)]
        number = tmpData.shape[0]
        admitTime = pd.to_datetime(tmpData["采血时间"].iloc[0])
        curTime = admitTime
        for i in range(number):
            prevTime = curTime
            curTime = pd.to_datetime(tmpData["采血时间"].iloc[i])
            tmpData["采血日期"].iloc[i] = curTime.date()  # 不是很确定
            if ((curTime - prevTime).days < 21):
                tmpData["admitNo_modify"].iloc[i] = "{}-{}{}".format(ad, admitTime.year, admitTime.month)
            else:
                admitTime = curTime
                tmpData["admitNo_modify"].iloc[i] = "{}-{}{}".format(ad, admitTime.year, admitTime.month)
        pData = pd.concat([pData, tmpData])
    df = pData
    #pData.to_excel("test.xlsx")

def summary_glucose_number():
    admitList = set(df["admitNo_modify"])
    patientList = load_patient_list(admitList)
    dayList = load_patient_day_list(patientList)

    set_exam_item(patientList)
    patientDayList = set_exam_item_based_on_day(patientList, dayList)

    print("finish step 1")
    psList = set_glucose_item(patientList)
    psDayList = set_glucose_item_on_day(patientDayList)

    #print_patient_summary(psList)
    print_to_excel(psList, psDayList)
    print("finish step 2")

def main():
    update_admit_no()
    summary_glucose_number()

if __name__ == "__main__":
    main()
    print("end")