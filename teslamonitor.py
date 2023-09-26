import requests
import json
import urllib
import os.path
from requests.adapters import HTTPAdapter, Retry

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
	"outsideSearch": False
}

queryString = json.dumps(queryJson)

url = 'https://www.tesla.com/inventory/api/v1/inventory-results?query=' + urllib.parse.quote(queryString)

print(url)
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
headers['Accept'] = 'application/json'

s = requests.Session()

retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 403, 500, 502, 503, 504 ])

s.mount('https://', HTTPAdapter(max_retries=retries))

teslaRequest = s.get(url, timeout=10, allow_redirects = True, headers=headers)

if teslaRequest.ok and teslaRequest.status_code == 200:
	teslaResponse = json.loads(teslaRequest.content)
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
	print('"Request error: ' + str(teslaRequest.status_code) + '."' )