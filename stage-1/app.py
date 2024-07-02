from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# def get_location_info(ip_address):
#     # Use a service like ipinfo.io to get location info
#     response = requests.get(f"https://ipinfo.io/{ip_address}/json")
#     data = response.json()
#     print(f"ip_info_data: {data}")
#     city = data.get("city", "Unknown")
#     return city

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip

def get_temperature(city):
    # Use a weather API to get the temperature. For example, OpenWeatherMap.
    api_key = os.environ["api_key"]
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    data = response.json()
    print(f"Temperature data: {data}")
    temperature = data['main']['temp']
    return temperature

@app.route('/', methods=['GET'])
@app.route('/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = request.remote_addr
    print(f"client IP: {client_ip}")
    location = get_location_info(client_ip)
    temperature = get_temperature(location)

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
