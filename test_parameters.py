import pytest
from playwright.sync_api import sync_playwright
import time
import pandas as pd
import mysql.connector
from openpyxl import Workbook
from mysql_connection import MySQLConnection
from decimal import Decimal
import pytest_check as check

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",              # your MySQL username
#     password="Root@123",      # your MySQL password
#     database="mysql"        # your database name
# )
#
# cursor = conn.cursor()
db= MySQLConnection()
db.setup_connection()

@pytest.mark.parametrize("region,country,city",[("Asia","India","Mumbai"),("Asia","China","Beijing"),("Europe","Germain","Berlin")])
def test_run(region,country,city):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set True for headless mode
        page = browser.new_page()

        page.goto("https://app.fabric.microsoft.com/home?experience=fabric-developer")
        page.locator("#email").fill('sakthivel.seeniv@tigeranalytics.com')
        page.locator("#submitBtn").click()
        page.get_by_placeholder("Password").fill("Sakthi@612")
        page.locator("input[value='Sign in']").click()
        page.locator("input[value='Yes']").click()
        page.locator("//span[text()='Workspaces']").click()
        page.locator("button[title='My workspace']").click()
        page.get_by_placeholder("Filter by keyword").fill("Sales")
        page.locator("(//a[text()=' Sales Dashboard '])[1]").click()

        df = pd.read_excel("C:\\Users\\sakthivel.seeniv\\Downloads\\Excel_Test_Data.xlsx")
        wb = Workbook()
        ws = wb.active
        ws.title = "Test Report"
        ws.append(["Region", "Country", "City", "Total Sales", "Total Profit", "Total Sales DB", "Total Profit DB",
                   "Sales BI vs DB", "Profit BI vs DB"])
        row_no = 0
        row_no = row_no + 1
        region = region
        country = country
        city = city

        elmt = page.locator("//button[@class='resetBtn rightActionBarBtn app-bar-nav-btn ng-star-inserted']")
        if elmt.is_enabled():
            elmt.click()
            page.locator("//button[text()='Reset']").click()
            time.sleep(3)

        elements = page.locator("//div[contains(@class,'card categorical')]").all()
        for e in elements:
            searchKey = ''
            if "Region" in e.text_content():
                searchKey = region
            if "Country" in e.text_content():
                searchKey = country
            if "City" in e.text_content():
                searchKey = city
            e.click()
            time.sleep(3)
            e.locator("//input[@placeholder='Search']").type(searchKey)
            time.sleep(5)
            e.locator("(//span[@class='glyphicon checkbox checkboxOutline'])[1]").click()

        time.sleep(3)
        totalSales = float(
            page.locator("(//div[@class='visualWrapper report'])[2]").text_content().replace("Total Sales",
                                                                                             "").replace(",",
                                                                                                         ""))
        totalProfit = float(
            page.locator("(//div[@class='visualWrapper report'])[3]").text_content().replace("Total Profit",
                                                                                             "").replace(",",
                                                                                                         ""))
        query = f"SELECT * FROM sales_table where place='{city}'"
        results = db.execute_query(query)

        print("Region : ", region, ", Country : ", country, ", City : ", city, totalSales, totalProfit,
              results[0][2], results[0][3])
        ws.append(
            [region, country, city, totalSales, totalProfit, results[0][2], results[0][3], f"=D{row_no}=F{row_no}",
             f"=E{row_no}=G{row_no}"])

        # assert Decimal(str(totalSales)) == Decimal(results[0][2])
        # assert Decimal(str(totalProfit)) == Decimal(results[0][3])
        check.equal(Decimal(str(totalSales)), Decimal(results[0][2]))
        check.equal(Decimal(str(totalProfit)), Decimal(results[0][3]))

        wb.save("C:\\Users\\sakthivel.seeniv\\Downloads\\Test_Result_Report.xlsx")

        #page.screenshot(path="example.png")
        time.sleep(5)
        #print("Page title:", page.title())
        browser.close()
        #db.close_connection()

