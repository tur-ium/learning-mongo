"""
Get Weather Data for known cities (listed in a Mongo database of zip codes
and store to a new MongoDB collection

"""
import datetime
import re
import dotenv
import os
import httpx
import pymongo
from pprint import pprint

get_from_api = True

dotenv.load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
print(OPENWEATHER_API_KEY)
if get_from_api and OPENWEATHER_API_KEY is None:
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

for city_data in c_zips.find({}, {'city':1,'zip':1}).limit(5):
    pprint(city_data['city'])
    lookup = f"{city_data['city']},{city_data['zip']},US"
    if get_from_api is True:
        print('Getting result from API')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={lookup}&appid={OPENWEATHER_API_KEY}'
        weather_data = httpx.get(url)
        weather_data = weather_data.json()
    else:
        print('Getting stored result')
        stored_weather_data = c_weather.find({'name': re.compile(city_data['city'], re.IGNORECASE)}).sort('dt', direction=-1).limit(1)
        weather_data = stored_weather_data.next()

    weather_contents = weather_data['weather']
    main_contents = weather_data['main']
    cleaned_weather_data = {}
    cleaned_weather_data.update({'main': main_contents})
    cleaned_weather_data.update({'weather': weather_contents})
    cleaned_weather_data.update({'city':city_data['city'],
                                 'time':datetime.datetime.fromtimestamp(weather_data['dt']).strftime('%H:%M:%S')})
    c_weather.insert_one(cleaned_weather_data)

    # Retrieve the documents where the main subkey is "Clear" and display only the name of the city without the document ID :
clear_weather = c_weather.find({'weather.main':'Clear'},{'city':1,'weather.main':1,'_id':0}).sort('dt', direction=-1)
print('Cities with clear weather right now',[x for x in clear_weather])

# How many cities have temp_min greater than or equal to 281 and a key value temp_max less than or equal to 291 (temperatures are in Kelvin)
cities_in_temp_range = [x for x in c_weather.find({'$and':[{'main.temp_min':{'$gte':281}},{'main.temp_max':{'$lte':291}}]})]
print(f'Cities with current temp between 281 K (7.85C) and 291K (17.85C): {len(cities_in_temp_range)}')

# Return the number of documents we have according to the weather.main subkey
count_cities_with_weather_main_subkey = len([x for x in c_weather.find({'weather.main':{'$exists':True}})])
print(f'Cities with weather.main subkey = {count_cities_with_weather_main_subkey}')