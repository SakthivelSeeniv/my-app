from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_element(driver,by,xpath,timeout=30):
    element=WebDriverWait(driver,timeout).until(
        EC.visibility_of_element_located((by,xpath))
    )
    time.sleep(3)
    return element

driver=webdriver.Chrome()
driver.get("https://app.fabric.microsoft.com/home?experience=fabric-developer")

# Maximize window
driver.maximize_window()
get_element(driver,By.ID,"email").send_keys('sakthivel.seeniv@tigeranalytics.com')
driver.find_element(By.ID,"submitBtn").click()
get_element(driver,By.NAME,"passwd").send_keys('Tiger#1234')
driver.find_element(By.XPATH,"//input[@value='Sign in']").click()
get_element(driver,By.XPATH,"//input[@value='Yes']").click()
get_element(driver,By.XPATH,"//span[text()='Workspaces']").click()
get_element(driver,By.XPATH,"//button[@title='My workspace']").click()
get_element(driver,By.XPATH,"//button[contains(@class,'import-button')]").click()
get_element(driver,By.XPATH,"//button[contains(.,'Report, Paginated Report or Workbook')]").click()
get_element(driver,By.XPATH,"//button[contains(.,'From this computer')]").click()
get_element(driver,By.XPATH, "//input[@type='file']").send_keys(r"C:\Users\sakthivel.seeniv\Downloads\Sales Dashboard Copy.pbix")
time.sleep(5)

driver.close()
