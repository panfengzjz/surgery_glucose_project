#coding: utf-8
import pandas as pd
import pickle
import time

from patientClass import Patient

def dump_pickle(fileName, patientList):
    with open(fileName, "wb") as f:
        pickle.dump(patientList, f)

def load_pickle(fileName):
    with open(fileName, "rb") as f:
        return pickle.load(f)

def load_admit_no(fn1, fn2, fn3):
    # fn1: 住院号文件名
    # fn2: 化验文件名
    # fn3: 手术文件名
    data1 = pd.read_excel(fn1)
    s1 = set(data1["住院号"])
    data2 = pd.read_excel(fn2)
    s2 = set(data2["门诊/住院号"])
    data3 = pd.read_excel(fn3)
    s3 = set(data3["admitno"])
    return list(s1 & s2 & s3)

def load_patient_list(fileName, anList):
    patientList = []
    data = pd.read_excel(fileName)
    for an in anList:
        pData = data.loc[data["门诊/住院号"] == an]
        if (pData.empty):
            continue
        adList = set(pData["入院时间"])
        for i in adList:
            patientList.append(Patient(an, i))
    return patientList

def set_exam_item(fileName, patientList):
    data = pd.read_excel(fileName)
    for p in patientList:
        pId = p.admitNo
        pAD = p.admitDate
        pData = data.loc[(data["门诊/住院号"] == pId)
                          & (data["入院时间"] == pAD)]
        if (pData.empty):
            continue
        p.set_basic_info(pData)

def set_surgery_item(fileName, patientList):
    data = pd.read_excel(fileName)
    for p in patientList:
        pId = p.admitNo
        pAD = p.admitDate
        pData = data.loc[(data["admitno"] == pId)
                          & (pd.to_datetime(data["admitdate"]) == pAD)]
        if (pData.empty):
            continue
        p.set_surgery_info(pData)

def set_glucose_item(fileName, patientList):
    data = pd.read_excel(fileName)
    for p in patientList:
        pId = p.admitNo
        pData = data.loc[data["姓名"] == pId]
        if (pData.empty):
            continue
        p.set_glucose_info(pData)

def main():
    baseFileName = "2016-2020外科部分POCT患者-住院号20210527.xlsx"
    examFileName = "20210723_sun_result.xlsx"
    surgeryFileName = "20210723_sun_result_surgery.xlsx"
    glucoseFileName2016 = "2016-glu处理后.xlsx"
    glucoseFileName2017 = "2017-glu处理后.xlsx"
    glucoseFileName2019 = "2019-glu处理后.xlsx"
    storeFileName = "sourceInfo.log"

    admitList = load_admit_no(baseFileName, examFileName, surgeryFileName)
    patientList = load_patient_list(examFileName, admitList)
    set_exam_item(examFileName, patientList)
    dump_pickle(storeFileName, patientList)
    set_surgery_item(surgeryFileName, patientList)
    dump_pickle(storeFileName, patientList)
    set_glucose_item(glucoseFileName2016, patientList)
    set_glucose_item(glucoseFileName2017, patientList)
    set_glucose_item(glucoseFileName2019, patientList)

    
    dump_pickle(storeFileName, patientList)
#    newData = load_pickle(storeFileName)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("end")
    print("cost time:", time.time() - start_time)
