import requests

def get_lat_long_opencage(address, api_key):
    # Fallback API key if not passed (replace with your own)
    if api_key is None:
        api_key = "026c50bfc71d48b183a7481884fb5c68"  # <-- put your OpenCage key here

    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            return latitude, longitude
    return None, None

# Usage example
api_key='026c50bfc71d48b183a7481884fb5c68'
restaurant_address = "1600 Amphitheatre Parkway, Mountain View, CA"
rest_lat, rest_long = get_lat_long_opencage(restaurant_address,api_key)
print(rest_lat, rest_long)
