import requests


def pullCurrent(query):
    response = requests.get('http://api.weatherapi.com/v1/current.json?',params={'query':query,'lang':'tr'},headers={'key':'f11585e962f84c82a8e90433242404'}  )
    if(response.status_code == 200):
        data = response.json()
        return {
            'status':0,
            'location':{
            'name': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country']
            },
            'weather':{
                'last_update':data['current']['last_updated'],
                'temp':data['current']['temp_c'],
                'condition':data['current']['condition']['text'],
                'humidity':data['current']['humidity'],
                'cloud':data['current']['cloud']
            }
        }
    else:
        return {
            'status':-1
        }
    
def pullForecast(query):
        response = requests.get('http://api.weatherapi.com/v1/forecast.json?',params={'query':query,'lang':'tr'},headers={'key':'f11585e962f84c82a8e90433242404'}  )


        if(response.status_code == 200):
            data = response.json()
            forecastData = list()

            for x in data['forecast']['forecastday'][0]['hour']:
                 forecastData.append({
                     'time':x['time'],
                     'temp':x['temp_c'],
                     'condition':x['condition']['text'],
                     'icon':x['condition']['icon'][2:],
                     'humidity':x['humidity']
                 })
                 

            return {
                'status':0,
                 'location':{
            'name': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country']
            },
            'forecast':forecastData
            }
            
        else:
            return {
                "status":-1
            }
            
def pullSuggestEssentials(query):
        response = requests.get('http://api.weatherapi.com/v1/forecast.json?',params={'query':query,'lang':'tr'},headers={'key':'f11585e962f84c82a8e90433242404'}  )

        if(response.status_code == 200):
            data = response.json()
            return {
                'status':0,
                'willRain':data['forecast']['forecastday'][0]['day']['daily_will_it_rain'],
                'willSnow':data['forecast']['forecastday'][0]['day']['daily_will_it_snow'],
                'avgtemp':data['forecast']['forecastday'][0]['day']['avgtemp_c'],
                'uv':data['forecast']['forecastday'][0]['day']['uv']
            }
            
        else:
            return {
                "status":-1
            }