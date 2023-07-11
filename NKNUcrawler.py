from time import sleep
import pymysql
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

class schCrawler():
    def __init__(self, id, password) -> None:
        self.id = id
        self.password = password
        self.db = pymysql.connect(host='localhost',
            user='root',
            password='910925As',
            database='nknustusch',
            autocommit=True)
        self.cursor = self.db.cursor()
        self.placeDict = {"CM": "寰宇大樓", "TC": "科技大樓", "MA": "致理大樓",
                "PH": "高斯大樓", "BT": "生科大樓", "LI": "圖書資訊大樓"}
        self.classTimeDict = {"1": "0810 ~ 0900", "2": "0901 ~ 1000", "3": "1001 ~ 1100",
                              "4": "1101 ~ 1200", "5": "1230 ~ 1320", "6": "1321 ~ 1420",
                              "7": "1421 ~ 1520", "8": "1521 ~ 1620", "9": "1621 ~ 1720",
                              "T": "1721 ~ 1820", "A": "1821 ~ 1910", "B": "1911 ~ 2005",
                              "C": "2006 ~ 2100", "D": "2101 ~ 2155", "E": "2156 ~ 2250"}
        
        self.driver = uc.Chrome(browser_executable_path=r"C:\Users\v99sa\Desktop\chrome-win\chrome.exe", options=self.__get_ChromeOptions(), version_main=110)
        self.driver.get('https://sso.nknu.edu.tw/userLogin/login.aspx?cUrl=/default.aspx')
        
        rawInfo = self.getRawInfo()
        classInfo = self.filterClassInfo(rawInfo)
        schInfo = self.filterSchInfo(rawInfo)
        if(self.isInDB()):
            pass
        else:
            self.addIntoDB(type="classInfo", input01=classInfo)
            self.addIntoDB(type="schInfo", input01=schInfo)
        self.driver.quit()
    
    def __get_ChromeOptions(self): 
                options = uc.ChromeOptions()
                options.add_argument('--start_maximized')
                options.add_argument("--disable-extensions")
                options.add_argument('--disable-application-cache')
                options.add_argument('--disable-gpu')
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-notifications")
                options.add_argument("--incognito")
                
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--user-data-dir=C:\\Users\\v99sa\\Desktop\\coding\\py\\pixiv-discord-bot\\profile1")
                return options
    
    def getRawInfo(self):
        wait = WebDriverWait(self.driver, 20)

        wait.until(EC.visibility_of_element_located((By.ID, "uLoginID")))
        username = self.driver.find_element(By.ID, "uLoginID")
        password = self.driver.find_element(By.ID, "uPassword")
        keepalive_button = self.driver.find_element(By.ID, "uKeepAlive_ssoLogin").click()
        login_button = self.driver.find_element(By.ID, "uLoginPassAuthorizationCode")

        username.send_keys(self.id)
        password.send_keys(self.password)
        login_button.click()


        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'課業')]")))
        class_button = self.driver.find_element(By.XPATH, "//a[contains(text(),'課業')]").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'學期課表')]")))
        class_schedule_button = self.driver.find_element(By.XPATH, "//a[contains(text(),'學期課表')]").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(),'E')]")))

        rows = self.driver.find_elements(By.XPATH, "//table/tbody")
        return rows

    def filterClassInfo(self, info):
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
        return classInfo
    def filterSchInfo(self, info):
        classInfo = info[0].text
        schInfo = info[1].text
        classInfo = classInfo.split("\n")
        classInfo.pop(0)
        
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
        
        return schInfo
    def isInDB(self):
        self.cursor.execute("SELECT id FROM stu_sch where id = '%s'" % self.id)
        results = self.cursor.fetchall()
        if(len(results) == 1):
            return True
        else:
            return False
    def addIntoDB(self, type, input01):
        if(type == "classInfo"):
            for c in input01:
                c = c.split(" ")
                c.pop(0)
                if(len(c) == 6):
                    c.pop(0)
                cDay = c[0][0]
                cTime = ""
                for i in c[0].split(","):
                    cTime += i[1] + " "
                cRoomNum = c[1]
                cRoomName = c[3]
                cTeacher = c[4].split("：")[0]
                self.cursor.execute("INSERT INTO `nknustusch`.`classInfo` (`id`, `cDay`, `cTime`, `cRoomNum`, `cRoomName`, `cTeacher`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (self.id, cDay, cTime, cRoomNum, cRoomName, cTeacher))
        elif(type == "schInfo"):
            timeNow = 0
            classTimes = self.classTimeDict.keys()
            
            for c in range(len(input01)):
                
                classTime = input01[c].split(" ")[0]
                if(classTime in classTimes and classTime > timeNow):
                    timeNow = classTime
                    
                    for i in range(c + 1, len(input01), 3):
                        try:
                            if(input01[i].split(" ")[0] in classTimes):
                                break
                        except:
                            break
                        sTime = input01[c]
                        cName = input01[i]
                        cTeacher = input01[i + 1]
                        cRoomNum = input01[i + 2].split(" - ")[0]
                        cRoomName = input01[i + 2].split(" - ")[1]
                        
                        self.cursor.execute("INSERT INTO `nknustusch`.`schInfo` (`id`, `sTime`, `cName`, `cTeacher`, `cRoomNum`, `cRoomName`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (self.id, sTime, cName, cTeacher, cRoomNum, cRoomName))
                    

#schC = schCrawler("411077002", "home0857")
schC = schCrawler("411077016", "910925as")
