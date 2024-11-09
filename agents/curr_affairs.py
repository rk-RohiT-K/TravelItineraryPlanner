import requests
from fastapi import FastAPI
import ollama

app = FastAPI()

newsapi = 'YOUR_API_KEY'
weatherapi = 'YOUR_API_KEY'

news_url = f'https://newsapi.org/v2/everything?q={{}}&from={{}}&sortBy=popularity&apiKey={newsapi}'
weather_url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{{}}?apikey={weatherapi}'
weather_location = f'http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={weatherapi}&q={{}}'

def get_news(region: str):
    """
    Fetch top 10 news articles based on region (city or country).
    """
    url = news_url.format(region, "2024-11-09")
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        print(news_data)
        articles = news_data.get('articles', [])
        
        news_descriptions = [article['description'] for article in articles[:10]]
        return news_descriptions
    else:
        return []

def get_weather(location: str):
    """
    Fetch the weather information for a given location.
    """
    # Get location key based on city name
    location_url = weather_location.format(location)
    location_response = requests.get(location_url)
    
    if location_response.status_code == 200:
        location_data = location_response.json()
        location_key = location_data[0]['Key']
        
        # Get weather forecast using the location key
        weather_response = requests.get(weather_url.format(location_key))
        
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            # Retrieve weather information text (Headline['Text'])
            weather_text = weather_data['Headline']['Text']
            # print(weather_text)
            return weather_text
        else:
            return f"Weather Error: {weather_response.status_code}"
    else:
        return f"Location Error: {location_response.status_code}"

def generate_safety_assessment(news: str, weather: str):
    """
    Generate a safety assessment from the news and weather information using Ollama 3.2 model.
    """
    prompt = f"""
    Based on the following news and weather information, assess whether it is safe to tour the city. Just mention which places or time of day to avoid only if conditions are severe rest just output okay.
    
    News:
    {news}
    
    Weather:
    {weather}
    
    Respond with a brief assessment: is it safe to travel? what arrangement for weather have to be done?
    """
    
    response = ollama.chat(model="llama3.2", prompt=prompt)
    return response['message']['content']

@app.get("/get_news_and_weather/")
async def get_news_and_weather(region: str):
    # Get news articles descriptions
    news_descriptions = get_news(region)
    
    # Get weather information
    weather_info = get_weather(region)
    
    if isinstance(news_descriptions, list) and weather_info:
        news_text = '\n'.join(news_descriptions)  # Combine the top 10 news descriptions
        safety_assessment = generate_safety_assessment(news_text, weather_info)
        return safety_assessment
    else:
        return {"error": "Failed to retrieve news or weather data."}

