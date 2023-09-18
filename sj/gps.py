import requests
import os
from dotenv import load_dotenv
import json


def get_gps():
    load_dotenv()
    google_maps_api_key = os.environ.get('google_maps_api_key')
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={google_maps_api_key}'

    response = json.loads(requests.post(url).text)
    
    location = response['location']
    lat = round(location['lat'], 2)
    lng = round(location['lng'], 2)
    lat_lng = [lat, lng]
    print(lat_lng)
    
    return lat_lng


if __name__ == "__main__":
    get_gps()
