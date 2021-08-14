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
        pData = data.loc[data["住院号"] == pId]
        if (pData.empty):
            continue
        p.set_glucose_info(pData)

def dump_patient_data():
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
    print("finish step 1")
    set_surgery_item(surgeryFileName, patientList)
    dump_pickle(storeFileName, patientList)
    print("finish step 2")
    set_glucose_item(glucoseFileName2016, patientList)
    set_glucose_item(glucoseFileName2017, patientList)
    set_glucose_item(glucoseFileName2019, patientList)
    dump_pickle(storeFileName, patientList)
    print("finish step 3")

def flatten_inpatient(patientList):
    dfColumns = ["住院号", "姓名", "性别", "年龄", "科室", "入院日期", "住院时长",
                 "手术1-admitdiag", "手术1-applytime", "手术1-presurgery",
                 "手术1-surgeryname", "手术1-surgerytype", "手术1-surgerykind",
                 "手术2-admitdiag", "手术2-applytime", "手术2-presurgery",
                 "手术2-surgeryname", "手术2-surgerytype", "手术2-surgerykind",
                 "手术3-admitdiag", "手术3-applytime", "手术3-presurgery",
                 "手术3-surgeryname", "手术3-surgerytype", "手术3-surgerykind",
                 "手术4-admitdiag", "手术4-applytime", "手术4-presurgery",
                 "手术4-surgeryname", "手术4-surgerytype", "手术4-surgerykind",
                 "first-fpg", "first-hb", "first-cr", "first-alt", "first-ast",
                 "ap-fpg", "ap-hb", "ap-cr", "ap-alt", "ap-ast",
                 "术前平均血糖", "术后最高血糖", "术后平均血糖", "是否有30天内再入院"]
    pData = pd.DataFrame(columns=dfColumns)
    print(pData.shape[0], pData.shape[1])
    for p in patientList:
        tmpData = pd.DataFrame(columns=dfColumns)
        tmpData["住院号"] = [p.admitNo]
        tmpData["姓名"] = [p.name]
        tmpData["性别"] = [p.gender]
        tmpData["年龄"] = [p.age]
        tmpData["科室"] = [p.deptName]
        tmpData["入院日期"] = [p.admitDate]
        tmpData["住院时长"] = [p.los]
        for i in range(len(p.surgeryList)):
            tmpData["手术{}-admitdiag".format(i+1)] = [p.surgeryList[i][0]]
            tmpData["手术{}-applytime".format(i+1)] = [p.surgeryList[i][1]]
            tmpData["手术{}-surgerykind".format(i+1)] = [p.surgeryList[i][2]]
            tmpData["手术{}-surgeryname".format(i+1)] = [p.surgeryList[i][3]]
            tmpData["手术{}-surgerytype".format(i+1)] = [p.surgeryList[i][4]]
            tmpData["手术{}-surgerykind".format(i+1)] = [p.surgeryList[i][5]]
        tmpData["first-fpg"] = [p.exam.fpgDict.get(min(p.exam.fpgDict.keys(), default=pd.NA), pd.NA)]
        tmpData["first-hb"] = [p.exam.hbDict.get(min(p.exam.hbDict.keys(), default=pd.NA), pd.NA)]
        tmpData["first-cr"] = [p.exam.crDict.get(min(p.exam.crDict.keys(), default=pd.NA), pd.NA)]
        tmpData["first-alt"] = [p.exam.altDict.get(min(p.exam.altDict.keys(), default=pd.NA), pd.NA)]
        tmpData["first-ast"] = [p.exam.astDict.get(min(p.exam.astDict.keys(), default=pd.NA), pd.NA)]
        
        if (len(p.surgeryList) != 0):
            maxFpg = 0
            for i in p.exam.fpgDict.keys():
                if (p.surgeryList[0][1] < i < p.dischargeDate):
                    maxFpg = max(maxFpg, p.exam.fpgDict[i])
            tmpData["ap-fpg"] = [maxFpg] if (maxFpg) else [pd.NA]
            
            maxHb = 0
            for i in p.exam.hbDict.keys():
                if (p.surgeryList[0][1] < i < p.dischargeDate):
                    maxHb = max(maxHb, p.exam.hbDict[i])
            tmpData["ap-hb"] = [maxHb] if (maxHb) else [pd.NA]
            
            maxCr = 0
            for i in p.exam.crDict.keys():
                if (p.surgeryList[0][1] < i < p.dischargeDate):
                    maxCr = max(maxCr, p.exam.crDict[i])
            tmpData["ap-cr"] = [maxCr]  if (maxCr) else [pd.NA]
            
            maxAlt = 0
            for i in p.exam.altDict.keys():
                if (p.surgeryList[0][1] < i < p.dischargeDate):
                    maxAlt = max(maxAlt, p.exam.altDict[i])
            tmpData["ap-alt"] = [maxAlt] if (maxAlt) else [pd.NA]
            
            maxAst = 0
            for i in p.exam.astDict.keys():
                if (p.surgeryList[0][1] < i < p.dischargeDate):
                    maxAst = max(maxAst, p.exam.astDict[i])
            tmpData["ap-ast"] = [maxAst] if (maxAst) else [pd.NA]
            beforeGlu = 0
            afterGlu = 0
            maxGlu = 0
            gluLen = len(p.glucose.time)
            if (gluLen == 0):
                tmpData["术前平均血糖"] = pd.NA
                tmpData["术后平均血糖"] = pd.NA
                tmpData["术后最高血糖"] = pd.NA
            else:
                for i in range(gluLen):
                    if (p.admitDate < p.glucose.time[i] < p.surgeryList[0][1]):
                        beforeGlu += p.glucose.glu[i]
                    elif (p.surgeryList[0][1] < p.glucose.time[i] < p.dischargeDate):
                        afterGlu += p.glucose.glu[i]
                        maxGlu = max(maxGlu, p.glucose.glu[i])
                tmpData["术前平均血糖"] = [beforeGlu / gluLen]
                tmpData["术后平均血糖"] = [afterGlu / gluLen]
                tmpData["术后最高血糖"] = [maxGlu]
        
        pData = pd.concat([pData, tmpData])
    # end for p in patientList
    pData.to_excel("test.xlsx")

def main():
    storeFileName = "sourceInfo.log"
    dump_patient_data()
    newData = load_pickle(storeFileName)
    flatten_inpatient(newData)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("end")
    print("cost time:", time.time() - start_time)
