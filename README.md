# TeslaMonitor

*Script to track Tesla's inventory*

This script allows to easy track Tesla's inventory using inventory API (this is not a web page scraper).

Script can be run from command line or automaticaly using in example cron.
Found cars are displayed on console, script allows also to send push notification to your phone using [Pushover](https://pushover.net)
Script sends only one notication per car (per vin exactly)

## Install

### Requirements

- Installed python3
- Installed pip (in some situations can be useful)
- Installed Selenium for teslamonitorselenium.py

### Instalation

Clone that repository or simply download teslamonitor.py file to local folder. Then follow instructions from [Configuration](#configuration) chapter.

## Configuration

Configuration occurs on the beginning of script. You can set keys neccessary to use Pushover and model of Tesla you are looking for.

### Pushover
To use Pushover you should register on [Pushover](https://pushover.net), obtain user key and token, set it in the file and then install Pushover mobile app on your phone.

- pushoverToken - set to token obtained from Pushover or leave empty
- pushoverUserKey - set to user key obtained from Pushover or leave empty

### Car model and equipment

- model - set one of the following values:  my, m3, ms, mx

Example:
```
model = "my"
```

- version (aka trim) - choose from the following values:
  - for Tesla Y: RAWD, LRAWD, MYRWD
  - for Tesla 3: LRAWD, LRRWD, M3RWD
  - for Tesla X: MXPLAID, MXAWD
  - for Tesla S: MSPLAID, MSAWD

You can choose more then one (separated commas), or leave empty if color doesn't matter.

Example:
```
version = ["MXPLAID"] # Tesla X PLAID
version = ["LRAWD", "MYRWD"] # Tesla Y AWD & RWD
version = [] # version doesn't matter
```

- condition - condition of your Tesla, possible values: new, used

Example:
```
condition = "new"
```

- colors - list of exterior paint colors, possible values: WHITE, BLACK, BLUE, SILVER, RED. You can choose more then one (separated commas), or leave empty if color doesn't matter.

Example:
```
colors = ["WHITE", "BLACK"] # colors white and black
colors = [] # colors doesn't matter
```

- wheels - wheels size for your car, possible values EIGHTEEN, NINETEEN, TWENTY, TWENTY_ONE, TWENTY_TWO. Not all sizes are available in every model. You can choose more then one (separated commas), or leave empty if wheels size doesn't matter.

Example:
```
wheels = ["NINETEEN", "TWENTY"] # wheels sizes 19" and 20"
wheels = [] # wheels size doesn't matter
```

- towing - To add towing option set to TOWING otherwise set empty

Example:
```
towing = "TOWING" # car with tow hitch
towing = "" # towing option doesn't matter
```

### Locale settings
Market and region settings.

Set three params:
- market
- region
- language

Get values from the table below.
| Country | language | market | region |
| --- | --- | --- | --- |
| Austria | de | AT | europe |
| Australia | en | AU | north america |
| Belgium | nl | BE | europe |
| Canada | en | CA | north america |
| Switzerland | de | CH | europe |
| Czechia | cs | CZ | europe |
| Germany | de | DE | europe |
| Denmark | da | DK | europe |
| Spain | es | ES | europe |
| Finland | fi | FI | europe |
| France | fr | FR | europe |
| United Kingdom | en | GB | europe |
| Greece | el | GR | europe |
| Croatia | hr | HR | europe |
| Hungary | hu | HU | europe |
| Ireland | en | IE | europe |
| Iceland | is | IS | europe |
| Italy | it | IT | europe |
| Luxembourg | fr | LU | europe |
| Mexico | es | MX | north america |
| Netherlands | nl | NL | europe |
| Norway | no | NO | europe |
| Poland | pl | PL | europe |
| Puerto Rico | es | PR | north america |
| Portugal | pt | PT | europe |
| Romania | ro | RO | europe |
| Sweden | sv | SE | europe |
| Slovenia | sl | SI | europe |
| United States | en | US | north america |


Example:
```
market = "PL"
region = "europe"
language = "pl"
```

### Location
Your location and range from your location to find a car

- zipCode - ZIP (postal) code of your location

Example:
```
zipCode = "00050"
```

- range - distance from your location to location of car. Set up to 200 (miles/kilometer) or 0 to find all deliverable cars.

Example:
```
zipCode = "0"
```

### Price
You can limit maximum price of car using that parameter.
- maxPrice - price in local currency, set to 0 if doesn't matter.

Example:
```
maxPrice = 250250
```


## Usage

You can run script directly from command line using:

```
python3 teslamonitor.py
```
or add teslamonitor.py to crontab (in some cases additional shell script `teslamonitor.sh` can be required).

Example of usage of cron to run monitor every 15 minutes

```
*/15 * * * * root /path_to_script/teslamonitor.sh >/dev/null
```

or 
```
*/15 * * * * cd  /path_to_script/ && python3 teslamonitor.py > /dev/null
```

All depends on version of operating system and cron you use.