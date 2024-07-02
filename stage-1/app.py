from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip

def get_location_info(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    return data

def get_temperature_and_city(ip_address):
    location_data = get_location_info(ip_address)
    
    city = location_data.get("city", "Unknown")
    if city == "Unknown":
        return city, 0  # Default temperature if city is not found

    api_key = os.environ["api_key"]
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    weather_data = response.json()

    if weather_data['cod'] != 200:
        return "Unknown", 0

    temperature = weather_data['main']['temp']
    city_name = weather_data.get('name', 'Unknown')
    
    return city_name, temperature

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = get_client_ip()

    city, temperature = get_temperature_and_city(client_ip)
    
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
