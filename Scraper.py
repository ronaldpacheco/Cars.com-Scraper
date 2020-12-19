from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import sqlite3


PATH ='D:\Desktop\Python\Selenium\chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH)
actions =ActionChains(driver)

def getPrice():
    try:
        price = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'vehicle-info__price'))).text
        if "Dealer" in price:
            price = price.split()
            price = price[0] + price[-1]
        return price
    except:
        return 0


def getLocation():
    try:
        temp = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'get-directions-link__link'))).text
        return temp
    except:
        return None

def getMileage():
    try:
        temp = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'vehicle-info__mileage'))).text
        return temp
    except:
        return None

#Test

carName = []
model = []
make = []
prices =[]
location =[]
mileage = []
seller = []
year = []
trim = []
tmp = []


for y in range(50):
    driver.get(f"https://www.cars.com/for-sale/searchresults.action/?page={y+1}&perPage=100&rd=99999&searchSource=PAGINATION&sort=relevance&zc=33761")
    time.sleep(15)
    cars = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing-row__title')))

    for car in cars:
        carName.append(car.text.split())

    for i in range(len(cars)):

        cars = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing-row__title')))

        try:
            cars[i].click()

            if len(getPrice())>1:
                seller.append('Dealer')
            else: seller.append("Private")
            prices.append(getPrice())
            year.append(carName[i][0])
            make.append(carName[i][1])
            trim.append(carName[i].pop())
            tmp=[]
            for x in range(len(carName[i][2:])):
                tmp.append(*carName[i][2+x:x+3])
            model.append(" ".join(tmp))

            mileage.append(getMileage())
            location.append(getLocation())
            driver.back()
        except:
            driver.get(f"https://www.cars.com/for-sale/searchresults.action/?page={y+1}&perPage=100&rd=99999&searchSource=PAGINATION&sort=relevance&zc=33761")

    time.sleep(1.5)

    carName = []
print(len(model), len(make))
df=pd.DataFrame({"Model" : model, "Make" : make, "Price": prices,
                "Location" : location, "Mileage" : mileage, "Seller" : seller, "Year" : year, "Trim" : trim
                })
conn = sqlite3.connect('CarData.db')

print(df)
df.to_sql('Cars', con=conn, if_exists='replace', index_label='id')
driver.quit()



