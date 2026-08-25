import json


# get data from json
with open("data/weatherData.json", "r") as file:
    weather_data = json.load(file)


# tool function
def get_weather(location: str):
    weather = weather_data.get(location)

    if not weather:
        return {
            "error": f"I don't have weather data for {location}."
        }

    return {
        "location": location,
        **weather
    }


# tool descriptor
get_weather_tool = {
    "name": "get_weather",
    "description": "Gets the current weather for a location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city to get the weather for."
            }
        },
        "required": ["location"]
    }
}
