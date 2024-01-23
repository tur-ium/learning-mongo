"""
Get Weather Data for known cities (listed in a Mongo database of zip codes
and store to a new MongoDB collection

"""
import dotenv
import os
import httpx
import pymongo
from pprint import pprint

get_from_api = False

dotenv.load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
print(OPENWEATHER_API_KEY)
if OPENWEATHER_API_KEY is None:
    raise ValueError('OpenWeather API key not defined')


client = pymongo.MongoClient(
    host="127.0.0.1",
    port=27017
)

sample = client['sample']
# Put the zips collection from the sample database into the c_zips variable and call the find_one method:

if 'weather' not in sample.list_collection_names():
    sample.create_collection('weather')

c_zips = sample['zips'] # MongoDB ZIP-code collection
c_weather = sample['weather'] # MongoDB weather collection

for city_data in c_zips.find({}, {'city':1,'zip':1}).limit(1):
    pprint(city_data['city'])
    lookup = f"{city_data['city']},{city_data['zip']},US"
    if get_from_api is True:
        print('Getting result from API')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={lookup}&appid={OPENWEATHER_API_KEY}'
        weather_data = httpx.get(url)
    else:
        print('Getting stored result')
        stored_weather_data = c_weather.find({'$match': {'name': city_data['city']}}).sort('dt', direction=-1).limit(1)
        weather_data = stored_weather_data
    pprint([x for x in weather_data])
    weather_contents = weather_data[0]['weather']
    main = weather_data[0]['main']
    cleaned_weather_data = {}
    cleaned_weather_data.update()
    c_weather.insert_one(weather_data.json())
