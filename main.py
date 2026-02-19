from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import mysql.connector
from openpyxl import Workbook


conn = mysql.connector.connect(
    host="localhost",
    user="root",              # your MySQL username
    password="Root@123",      # your MySQL password
    database="mysql"        # your database name
)

cursor = conn.cursor()

def wait_for_element_load(driver, by, value, timeout=30):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )
    time.sleep(2)
    return element


# Create Chrome browser instance
driver = webdriver.Chrome()

# Open a webpage
driver.get("https://app.fabric.microsoft.com/home?experience=fabric-developer")

# Maximize window
driver.maximize_window()
wait_for_element_load(driver,By.ID,"email")

driver.find_element(By.ID,"email").send_keys('sakthivel.seeniv@tigeranalytics.com')
driver.find_element(By.ID,"submitBtn").click()
wait_for_element_load(driver,By.NAME,"passwd")
driver.find_element(By.NAME,"passwd").send_keys('Tiger#1234')
driver.find_element(By.XPATH,"//input[@value='Sign in']").click()
wait_for_element_load(driver,By.XPATH,"//input[@value='Yes']")
driver.find_element(By.XPATH,"//input[@value='Yes']").click()
wait_for_element_load(driver,By.XPATH,"//span[text()='Workspaces']")
driver.find_element(By.XPATH,"//span[text()='Workspaces']").click()
wait_for_element_load(driver,By.XPATH,"//button[@title='My workspace']")
driver.find_element(By.XPATH,"//button[@title='My workspace']").click()
wait_for_element_load(driver,By.XPATH,"//input[@placeholder='Filter by keyword']")
driver.find_element(By.XPATH,"//input[@placeholder='Filter by keyword']").send_keys('Sales')
wait_for_element_load(driver,By.XPATH,"(//a[text()=' Sales Dashboard '])[1]")
driver.find_element(By.XPATH,"(//a[text()=' Sales Dashboard '])[1]").click()

df=pd.read_excel("C:\\Users\\sakthivel.seeniv\\Downloads\\Excel_Test_Data.xlsx")
wb=Workbook()
ws=wb.active
ws.title="Test Report"
ws.append(["Region", "Country", "City", "Total Sales", "Total Profit", "Total Sales DB", "Total Profit DB", "Sales BI vs DB", "Profit BI vs DB"])
row_no=0
for row in df.itertuples():
    row_no=row_no+1
    row_list=list(row)
    region=row_list[1]
    country = row_list[2]
    city = row_list[3]


    elmt=wait_for_element_load(driver,By.XPATH,"//button[@class='resetBtn rightActionBarBtn app-bar-nav-btn ng-star-inserted']")
    if elmt.is_enabled():
        elmt.click()
        wait_for_element_load(driver, By.XPATH,"//button[text()='Reset']").click()
        time.sleep(3)


    #wait_for_element_load(driver, By.XPATH,"//div[contains(@class,'card') and contains(normalize-space(),'Region')]").click()
    #wait_for_element_load(driver, By.XPATH,"//div[contains(@class,'card')]").click()
    #wait_for_element_load(driver, By.XPATH,"//span[text()='Sales Dashboard']").click()
    elements=driver.find_elements(By.XPATH,"//div[contains(@class,'card categorical')]")
    for e in elements:
        searchKey=''
        if "Region" in e.text:
            searchKey=region
        if "Country" in e.text:
            searchKey=country
        if "City" in e.text:
            searchKey=city
        e.click()
        time.sleep(3)
        e.find_element(By.XPATH,".//input[@placeholder='Search']").send_keys(searchKey)
        time.sleep(3)
        e.find_element(By.XPATH, "(.//span[@class='glyphicon checkbox checkboxOutline'])[1]").click()

    time.sleep(3)
    totalSales=float(driver.find_element(By.XPATH, "(//div[@class='visualWrapper report'])[2]").text.replace("Total Sales","").replace(",",""))
    totalProfit = float(driver.find_element(By.XPATH, "(//div[@class='visualWrapper report'])[3]").text.replace("Total Profit","").replace(",",""))
    query = f"SELECT * FROM sales_table where place='{city}'"
    cursor.execute(query)

    results = cursor.fetchall()

    print("Region : ",region, ", Country : ",country, ", City : ", city, totalSales, totalProfit, results[0][2], results[0][3])
    ws.append([region, country, city, totalSales, totalProfit, results[0][2], results[0][3], f"=D{row_no}=F{row_no}", f"=E{row_no}=G{row_no}"])



wb.save("C:\\Users\\sakthivel.seeniv\\Downloads\\Test_Result_Report.xlsx")
# Wait to see results
time.sleep(10)
print(driver.get_cookies())

# Close the browser
driver.quit()
