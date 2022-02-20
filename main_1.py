# coding: utf-8
import pandas as pd
from patientCLass_1 import Patient
from patientCLass_1 import PatientSummary

fileName = "基线2015-2017内分泌所有住院血糖.xlsx"
df = pd.read_excel(fileName)

def load_admit_no():
    return set(df["住院号"])

def load_patient_list(anList):
    patientList = []
    for an in anList:
        pData = df.loc[df["住院号"] == an]
        if (pData.empty):
            continue
        patientList.append(Patient(an))
    return patientList

def set_exam_item(patientList):
    for p in patientList:
        pId = p.admitNo
        pData = df.loc[(df["住院号"] == pId)]
        if (pData.empty):
            continue
        p.set_basic_info(pData)
        p.set_glucose_info(pData)

def set_glucose_item(patientList):
    psList = []
    for p in patientList:
        ps = PatientSummary()
        ps.set_basic_info_s(p)
        ps.set_glucose_info_s(p.glucose)
        psList.append(ps)
    return psList

def print_patient_summary(psList):
    for ps in psList:
        ps.print_glucose()

def print_to_excel(psList):
    dfColumns = ["住院号", "姓名", "年龄", "性别", "采血时间", "是否七个时刻都有血糖监测",
                 "所有血糖总条数", "所有血糖均值", "所有血糖标准差", "所有血糖最小值", "所有血糖最大值",
                 ">13.9比例", ">10比例", "3.9~10比例", "<3.9比例", "<3.0比例",
                 "餐前血糖总条数", "餐前血糖均值", "餐前血糖标准差", "餐前血糖最小值", "餐前血糖最大值",
                 "餐后血糖总条数", "餐后血糖均值", "餐后血糖标准差", "餐后血糖最小值", "餐后血糖最大值",
                 "睡前血糖总条数", "睡前血糖均值", "睡前血糖标准差", "睡前血糖最小值", "睡前血糖最大值"]
    pData = pd.DataFrame(columns=dfColumns)
    for ps in psList:
        tmpData = pd.DataFrame(columns=dfColumns)
        tmpData["住院号"] = [ps.admitNo]
        tmpData["姓名"] = [ps.name]
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
        pData = pd.concat([pData, tmpData])
    pData.to_excel("result.xlsx")

def summary_glucose_number():
    admitList = load_admit_no()
    patientList = load_patient_list(admitList)
    set_exam_item(patientList)
    print("finish step 1")
    psList = set_glucose_item(patientList)
    #print_patient_summary(psList)
    print_to_excel(psList)

def main():
    summary_glucose_number()

if __name__ == "__main__":
    main()
    print("end")