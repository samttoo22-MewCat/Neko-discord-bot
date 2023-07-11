from datetime import datetime


def isInDB(self):
        self.cursor.execute("SELECT id FROM stu_sch where id = '%s'" % self.id)
        results = self.cursor.fetchall()
        if(len(results) == 1):
            return True
        else:
            return False
def addIntoDB(self):
    outSch = ""
    day = 1
    self.cursor.execute("INSERT INTO `nknustusch`.`stu_sch` (`id`) VALUES ('%s')" % (self.id))
    for daySch in self.sch:
        for i in daySch:
            outSch = outSch + " " + i
        self.cursor.execute("update stu_sch set day0%s = '%s' where id = '%s'" % (str(day), outSch, self.id))
        day += 1
        outSch = ""
    print(outSch)
def getSchFromDB(self):
    out = [[], [], [], [], [], [], []]
    for day in range(1, 8):
        self.cursor.execute("select day0%s from stu_sch where id = '%s'" % (str(day), self.id))
        daySch = self.cursor.fetchone()
        daySch = daySch[0].split(" ")
        daySch.pop(0)
        temp = ""
        for i in range(0, len(daySch), 3):
            temp = daySch[i] + " " + daySch[i + 1] + " " + daySch[i + 2]
            out[day - 1].append(temp)
            temp = ""
    return out
def filterInfo(self, info):
    classInfo = info[0].text
    schInfo = info[1].text
    classInfo = classInfo.split("\n")
    classInfo.pop(0)
    print("classInfo")
    print(classInfo)
    
    for i in range(len(schInfo)):
        try:
            if(schInfo[i] == "~"):
                schInfo = schInfo[:i-1] + schInfo[i:]
                schInfo = schInfo[:i] + schInfo[i+1:]
        except:
            pass
    schInfo = schInfo.split("\n")
    for i in range(len(schInfo)):
        if("SM" in schInfo[i]):
            schInfo[i] = schInfo[i].split("SM")[0]
        elif("GR" in schInfo[i]):
            schInfo[i] = schInfo[i].split("GR")[0]
    schInfo.pop(0)
    print("schInfo")
    print(schInfo)
    
    finalInfo = [[], [], [], [], [], [], []]
    for i in range(len(classInfo)):
        temp = classInfo[i].split(" ")
        temp = temp[1]
        classDay = temp.split(",")[0][0]
        classTime = []
        for j in temp.split(","):
            classTime.append(j[1])
        teacher = temp[len(temp) - 1]
        for j in range(len(schInfo)):
            info = schInfo[j].split(" ")
            classTimeList = ["1", "2", "3", "4", "5", "6", "7"
                                , "8", "9", "A", "B", "C", "D", "E"]
            
            for cTime in classTime:
                #代表目前classInfo的課找到了對應schInfo的課堂
                if(info[0] in classTimeList and info[0] == cTime):
                    teacherInSch = schInfo[j + 2]
                    if(teacherInSch == teacher):
                        finalInfo[classDay - 1].append()
        
    
    print("finalInfo")
    print(finalInfo)  
    self.driver.quit()            
    return finalInfo     
def getCurrentClass(self):
    #currentTime = datetime.now().strftime("%H:%M:%S")
    currentTime = datetime.strptime("04:55:00", "%H:%M:%S")
    weekday = datetime.now().weekday()
    daySch = self.sch[weekday]
    #currentTime = time
    times = list(self.classTimeDict.values())
    output = ""
    todayClassTime = []
    
    for i in daySch:
        i = i.split(" ")
        todayClassTime.append(i[0])
    
    b = False
    for time in todayClassTime:
        time = self.classTimeDict[time]
        orginalTime = time
        time = time.split(" ~ ")
        time01 = datetime.strptime(time[0], "%H%M")
        time02 = datetime.strptime(time[1], "%H%M")
        time03 = datetime.strptime("0810", "%H%M")
        time04 = datetime.strptime("2250", "%H%M")
        cTime = datetime.strptime(currentTime.strftime("%H:%M:%S"), "%H:%M:%S")
        if(b):
            break
        if(cTime > time01 and cTime < time02):
            classTimeNumber = list(self.classTimeDict.keys())
            classTimeNumber = classTimeNumber[times.index(orginalTime)]
            
            for c in daySch:
                
                #c = c.split(" ")
                classTimeNumberInSch = c[0]
                if(classTimeNumber == classTimeNumberInSch):
                    output = c
                    b = True
                    break
        elif(cTime > time04):
            output = "今日所有課程已結束。"
            b = True
            break
        elif(cTime < time03):
            output = "-1"
            b = True
            break
    if(output == ""):
        output = "現在沒有課。"
    return output                  
def getClassTime(self, t):
    weekday = datetime.now().weekday()
    daySch = self.sch[weekday]
    currentTime = t
    times = list(self.classTimeDict.values())
    output = ""
    b = False
    for time in times:

        orginalTime = time
        time = time.split(" ~ ")
        time01 = datetime.strptime(time[0], "%H%M")
        time02 = datetime.strptime(time[1], "%H%M")
        time03 = datetime.strptime("0810", "%H%M")
        time04 = datetime.strptime("2250", "%H%M")
        cTime = datetime.strptime(currentTime.strftime("%H:%M:%S"), "%H:%M:%S")
        if(b):
            break
        if(cTime > time01 and cTime < time02):
            classTimeNumber = list(self.classTimeDict.keys())
            classTimeNumber = classTimeNumber[times.index(orginalTime)]
            
            for c in daySch:
                
                #c = c.split(" ")
                classTimeNumberInSch = c[0]
                if(classTimeNumber == classTimeNumberInSch):
                    output = classTimeNumberInSch
                    b = True
                    break
        elif(cTime > time04):
            output = "今日所有課程已結束。"
            b = True
            break
        elif(cTime < time03):
            output = "今日課程尚未開始。"
            b = True
            break
    if(output == ""):
        output = "現在沒有課。"
    return output
def getLastClass(self):
    pass
def getNextClass(self):
    weekday = datetime.now().weekday()
    daySch = self.sch[weekday]
    currentClass = self.getCurrentClass().split(" ")
    todayClassTime = []
    for i in daySch:
        i = i.split(" ")
        todayClassTime.append(i[0])
    if(len(currentClass) > 1):
        
        currentClassTime = currentClass[0]
        currentClassName = currentClass[1]
    else:
        if(currentClass[0] == "今日所有課程已結束。" or currentClass[0] == "現在沒有課。"):
            return "下堂沒有課"
        else:
            min = 999999
            for i in todayClassTime:
                i = int(i)
                if(i < min):
                    min = i
            currentClassTime = str(min)
            currentClassName = ""
    
    
    
    print(todayClassTime)
    for j in range(todayClassTime.index(currentClassTime), len(todayClassTime)):
        for i in daySch:
            temp = i.split(" ")
            classTime = temp[0]
            className = temp[1]

            if(classTime == todayClassTime[j] and className != currentClassName):
                return i      
        