import requests
import json
import urllib
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Pushover token that allows to send push notifications.
# Check pushover.net and obtain own tokens or leave empty to disable push notifications
pushoverToken = ''
pushoverUserKey = ''

# Model of your dream Tesla
# possible values: my, m3, ms, mx
model = "my" 

# Condition of your Tesla
# possible values: new, used
condition = "new"

# Car version
# Leave empty if doesn't matter, add more separated comma if you would select more then one
# Possible values: 
# for Tesla Y: RAWD, LRAWD, MYRWD
# for Tesla 3: LRAWD, LRRWD, M3RWD
# for Tesla X: MXPLAID, MXAWD
# for Tesla S: MSPLAID, MSAWD
version = ["LRAWD"]

# Additional car options

# Possible colors of car
# Leave empty if doesn't matter, add more separated comma if you would like to find more colors
# possible values: WHITE, BLACK, BLUE, SILVER, RED
colors = ["WHITE", "BLACK"]

# Possible wheels of car
# Leave empty if doesn't matter, add more separated comma if you would select more then one
# Possible values: EIGHTEEN, NINETEEN, TWENTY, TWENTY_ONE, TWENTY_TWO
# Not all sizes are available in every model
wheels = ["NINETEEN"]

# To add towing option set to TOWING otherwise set empty
towing = "TOWING"

# Market and region settings
# Check README for possible values
market = "PL"
region = "europe"
language = "pl"

# ZIP (postal) code of your location
zipCode = "00050"

# Range - distance from zip code to find car
# Possible value up to 200, set 0 if you would like to find all possible cars 
range = 0

#Maximum price in local currency
maxPrice = 0

# ---------      END CONFIGURATION 
# ---------------------------------------------------------------------------------------

carJson = {
	"model": model,
	"condition": condition
}

if len(colors) > 0 or len(wheels) > 0 or len(towing) > 0:
	optionsJson = {}
	if len(version) > 0:
		optionsJson["TRIM"] = version
	if len(colors) > 0:
		optionsJson["PAINT"] = colors
	if len(wheels) > 0:
		optionsJson["WHEELS"] = wheels
	if len(towing) > 0:
		optionsJson["ADL_OPTS"] = ["TOWING"]

	carJson["options"] = optionsJson
	
carJson["arrangeby"] = "Price"
carJson["order"] = "asc"
carJson["market"] = market
carJson["language"] = language
carJson["super_region"] = region
carJson["zip"] = zipCode
carJson["range"] = range

queryJson = {
	"query": carJson,
	"offset": 0,
	"count": 50,
	"outsideOffset": 0,
	"outsideSearch": False,
	"isFalconDeliverySelectionEnabled": False,
	"version": 0
}

queryString = json.dumps(queryJson)

url = 'https://www.tesla.com/inventory/api/v4/inventory-results?query=' + urllib.parse.quote(queryString)

print(url)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--window-size=0,0")
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
driver.get(url)

try: 
	content = driver.find_element(By.TAG_NAME, 'pre').text
except NoSuchElementException:
	content = ""

if len(content) > 0:
	teslaResponse = json.loads(content)
	resultCount = teslaResponse['total_matches_found']

	teslaResult = ('"Found ' + str(resultCount) + ' cars."\n')
	print(teslaResult)

	if int(resultCount) > 0:

		vins = []
		if os.path.exists("vins.txt"):
			with open('vins.txt') as filehandle:
				vins = json.load(filehandle)
			
		cars = teslaResponse['results']
		
		matchingCount = 0
		newCount = 0
		for car in cars:
			if car['Price'] <= maxPrice or maxPrice == 0:
				matchingCount = matchingCount + 1
				vin = car['VIN']
				if vin not in vins:
					newCount = newCount + 1
					vins.append(vin)
					link = 'https://www.tesla.com/' +language + '_' + market + '/' + model +  '/order/' + vin + '?referral=tomasz289218'
					print(link)
					message = 'Found new car. Direct link: \n' + link
				
					if len(pushoverToken) > 0:
						r = requests.post("https://api.pushover.net/1/messages.json", data = {
							"token": pushoverToken,
							"user": pushoverUserKey,
							"message": message
						})
						print(r.text)
				
		matchingStr = ('"Found ' + str(matchingCount) + ' matching cars. New cars ' + str(newCount) + '"\n')
		print(matchingStr)
		if len(vins) > 0:
			with open('vins.txt', 'w') as filehandle:
				json.dump(vins, filehandle)	
else: 
	print("Bad response")
