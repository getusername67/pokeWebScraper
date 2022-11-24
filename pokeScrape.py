#Matthew Sanders
#Scrapes raid pokemon data from thesilphroad.com and sends an email with the data
#Last edited 11/23/22

import math
import time
from selenium import webdriver
from selenium.webdriver import Chrome

"""
difficulty levels and their associated hex colors
dif0 = impossible
dif1 = hardcore
dif2 = hard
dif3 = medium
dif4 = easy
dif5 = very easy
dif6 = trivial
"""

#create driver
website = "https://thesilphroad.com/raid-bosses"
path = r"C:\Users\18506\Downloads\chromedriver_win32\chromedriver"
driver = webdriver.Chrome(path)
driver.get(website)

#collect data
raidBosses = []
#names
names = driver.find_elements("xpath", "//div[@class='boss-name']")
i = 0
for name in names:
    raidBosses.append([0 for x in range(4)])
    raidBosses[i][0] = name.text
    i += 1

#types
i = 0
allPokeTypes = driver.find_elements("xpath", "//div[@class='type-icons']")
for x in allPokeTypes:
    indivTypes = x.find_elements("xpath", "img")
    k = 0
    for y in indivTypes:
        deleteSubString1 = y.get_attribute("src").replace("https://assets.thesilphroad.com/img/pogo-assets/type-", "")
        deleteSubString2 = deleteSubString1.replace(".png", "")

        raidBosses[i][k+1] = deleteSubString2
        k += 1
    if raidBosses[i][2] == 0:
        raidBosses[i][2] = "none"
    i += 1

print(raidBosses)
#difficulties
i = 0
allPokemonDiffs = driver.find_elements("xpath", "//div[@class='hexagons']")
for x in allPokemonDiffs:
    indivDiffs = x.find_elements("xpath", "div")
    diffs = []
    for y in indivDiffs:
        diffNum = y.get_attribute("class").replace("hexagon difficulty", "")
        diffs.append(diffNum)
    recommendedGroupSize = 0
    while int(diffs[recommendedGroupSize]) < 3:
        recommendedGroupSize += 1
    raidBosses[i][3] = recommendedGroupSize + 1
    i += 1

#send to email

while True:
    pass

