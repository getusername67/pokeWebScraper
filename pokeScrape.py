#Matthew San
#Scrapes raid pokemon data from thesilphroad.com and sends an email with the data
#Last edited 11/23/22

import time
from selenium import webdriver
from selenium.webdriver import Chrome

#type images
fightingImg = "https://assets.thesilphroad.com/img/pogo-assets/type-fighting.png"
fireImg = "https://assets.thesilphroad.com/img/pogo-assets/type-fire.png"
grassImg = "https://assets.thesilphroad.com/img/pogo-assets/type-grass.png"
steelImg = "https://assets.thesilphroad.com/img/pogo-assets/type-steel.png"
fairyImg = "https://assets.thesilphroad.com/img/pogo-assets/type-fairy.png"
ghostImg = "https://assets.thesilphroad.com/img/pogo-assets/type-ghost.png"
bugImg = "https://assets.thesilphroad.com/img/pogo-assets/type-bug.png"
electricImg = "https://assets.thesilphroad.com/img/pogo-assets/type-electric.png"
groundImg = "https://assets.thesilphroad.com/img/pogo-assets/type-ground.png"
iceImg = "https://assets.thesilphroad.com/img/pogo-assets/type-ice.png"
dragonImg = "https://assets.thesilphroad.com/img/pogo-assets/type-dragon.png"
darkImg = "https://assets.thesilphroad.com/img/pogo-assets/type-dark.png"
waterImg = "https://assets.thesilphroad.com/img/pogo-assets/type-water.png"
flyingImg = "https://assets.thesilphroad.com/img/pogo-assets/type-flying.png"
psychicImg = "https://assets.thesilphroad.com/img/pogo-assets/type-psychic.png"
normalImg = "https://assets.thesilphroad.com/img/pogo-assets/type-normal.png"
poisonImg = "https://assets.thesilphroad.com/img/pogo-assets/type-poison.png"
rockImg = "https://assets.thesilphroad.com/img/pogo-assets/type-rock.png"

#difficulty levels and their associated hex colors
dif0 = "5d5d5d"           #impossible
dif1 = "df562d"           #hardcore
dif2 = "e79b11"           #hard
dif3 = "f2d829"           #medium
dif4 = "A0DF3C"           #easy
dif5 = "25be46"           #very easy
dif6 = "13a591"           #trivial

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
    raidBosses[i][0] = name
    i += 1

i = 0
#types
allPokeTypes = driver.find_elements("xpath", "//div[@class='type-icons']")
for x in allPokeTypes:
    indivTypes = x.find_elements("xpath", "img")
    k = 0
    for y in indivTypes:
        print("types: " + y.get_attribute("src"))
        raidBosses[i][k+1] = y.get_attribute("src")
        k += 1
    if k == 1:
        raidBosses[i][2] = None

#difficulties
allPokemonDiffs = driver.find_elements("xpath", "//div[@class='hexagons']")
for x in allPokemonDiffs:
    indivDiffs = x.find_elements("xpath", "div")
    for y in indivDiffs:
        print("diff: " + y.get_attribute("class"))

#send to email

while True:
    pass

