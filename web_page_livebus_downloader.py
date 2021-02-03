import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import psycopg2

from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#connect to DB server
##try:
##    connection = psycopg2.connect("dbname='bustracker' user='postgres' password='passwordhere' host='pgserverhere' port='5432'")
##except:
##    print ("Unable to connect to database")

##cursor = connection.cursor()  
## pull data from webpage

url = 'https://tfe-opendata.com/api/v1/vehicle_locations'



def getwebdata():
    response = requests.get(url,verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    updatetmstamp=-999
    try:
        data=json.loads(soup.contents[0])
        max = len(data['vehicles'])
    #print (max)
        updatetmstamp = data['last_updated']

        for i in range (0,max):
            gpsfix=data['vehicles'][i]['last_gps_fix']
            lat=data['vehicles'][i]['latitude']
            lng=data['vehicles'][i]['longitude']
            spd=data['vehicles'][i]['speed']
            heading=data['vehicles'][i]['heading']
            service=data['vehicles'][i]['service_name']
            vehicleid=data['vehicles'][i]['vehicle_id']
            journeyid=data['vehicles'][i]['journey_id']
            nextstop=data['vehicles'][i]['next_stop_id']
            destination=data['vehicles'][i]['destination']
        
            query =  "INSERT INTO buslog (updatetmstamp,gpsfix,lat,lng,spd,heading,service,vehicleid,journeyid,nextstop,destination) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            d = (updatetmstamp,gpsfix,lat,lng,spd,heading,service,vehicleid,journeyid,nextstop,destination)
##            cursor.execute(query, d)
            print (d)
        

##        connection.commit()
    except:
        print('error - webpage +JSON')
        time.sleep(10)

    return updatetmstamp

####################################

def run():
    lp=0
    while True:
        time.sleep(1)
        ret=getwebdata()
        lp=lp+1
        if lp==10:
            print (ret)
            lp=0


print ('running data collection')

while True:
    try:
        run()
    except:
        time.sleep(10)
        print ('?Woops - error')
        run()
