import requests
from dotenv import load_dotenv
import os

load_dotenv()


def pullCurrent(query):
    response = requests.get('http://api.weatherapi.com/v1/current.json?',params={'query':query},headers={'key':os.getenv('API_KEY')}  )
    if(response.status_code == 200):
        data = response.json()
        return {
            'location':{
            'name': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country']
            },
            'weather':{
                'last_update':data['current']['last_updated'],
                'temp':data['current']['temp_c'],
                'is_day':data['current']['is_day'],
                'condition':data['current']['condition']['text'],
                'icon':data['current']['condition']['icon'][2:],
                'wind_speed':data['current']['wind_mph'],
                'wind_dir':data['current']['wind_dir'],
                'humidity':data['current']['humidity'],
                'cloud':data['current']['cloud']
            }
        }
    else:
        return -1
    
def pullForecast(query):
        response = requests.get('http://api.weatherapi.com/v1/forecast.json?',params={'query':query},headers={'key':os.getenv('API_KEY')}  )


        if(response.status_code == 200):
            data = response.json()
            forecastData = list()
            forecastSummary = {
                  'maxtemp':data['forecast']['forecastday'][0]['day']['maxtemp_c'],
                      'mintemp':data['forecast']['forecastday'][0]['day']['mintemp_c'],
                      'avgtemp':data['forecast']['forecastday'][0]['day']['avgtemp_c'],
                'avghumidity':data['forecast']['forecastday'][0]['day'],
                'rain_chance':data['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
                'snow_chance':data['forecast']['forecastday'][0]['day']['daily_chance_of_snow'],
                'text':data['forecast']['forecastday'][0]['day']['condition']['text'],
                'icon':data['forecast']['forecastday'][0]['day']['condition']['icon'][2:],
            }

            for x in data['forecast']['forecastday'][0]['hour']:
                 forecastData.append({
                     
                 })
                 

            return {
                 'location':{
            'name': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country']
            },
            'summary':forecastSummary,
            'forecast':forecastData
            }
            
        else:
            return -1
      	

print(pullForecast('Pendik'))

