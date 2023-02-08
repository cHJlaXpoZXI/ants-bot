import requests
import datetime
from dateutil.relativedelta import *
import json
from discordwebhook import Discord

# Define date variable

today = datetime.datetime.today()
today = today.strftime('%Y-%m-%d')

# Parameters for API request

parameters = {
        "longitude":"-1.6777926",
        "latitude":"48.117266",
        "start_date":today,
        "end_date":"2023-06-30",
        "radius_km":"60",
        "address":"Rennes 35000",
        "reason":"PASSPORT",
        "documents_number":"2"
        }

# Request

request_data = requests.get("https://api.rendezvouspasseport.ants.gouv.fr/api/SlotsFromPosition", params=parameters)
data = request_data.json()

# Loop

if len(data) == 0:

    exit

else:

    city = data[0]['city_name']
    time = data[0]['available_slots'][0]['datetime']
    url = data[0]['available_slots'][0]['callback_url']
    date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+00:00')
    day = date.strftime('%d/%m/%Y')
    hour = date.strftime('%H:%M')
    
# Notification with Discord

    discord = Discord(url="https://discordapp.com/api/webhooks/")
    notification = "Un slot est disponible à {} le {} à {} ! Go check ici : {}".format(city, day, hour, url)
    discord.post(content=notification)
