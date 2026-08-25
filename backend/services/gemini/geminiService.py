import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# import tools
from services.gemini.tools.getWeather import get_weather
from services.gemini.tools.getWeather import get_weather_tool

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.5-flash-lite"


# main Gemini prompting function
def ask_gemini(prompt: str):

    contents = [
        types.Content(
            role = "user",
            parts = [
                types.Part.from_text(text=prompt)
            ]
        )
    ]

    while True:

        response = client.models.generate_content(
            model = MODEL,
            contents = contents,
            config = types.GenerateContentConfig(
                tools = [
                    types.Tool(
                        function_declarations = [
                            get_weather_tool
                        ]
                    )
                ]
            )
        )

        # preserve Gemini's response
        contents.append(response.candidates[0].content)

        # check if any function calls are necessary with the given prompt
        function_calls = []
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_calls.append(part.function_call)

        # if no function calls required, return
        if not function_calls:
            return response.text

        # execute functions
        function_responses = []
        for call in function_calls:

            print(f"Gemini called {call.name}")
            print("Arguments:", call.args)

            if call.name == "get_weather":
                result = get_weather(
                    call.args["location"]
                )
            else:
                result = {
                    "error": f"Unknown function: {call.name}"
                }

            print("Function result:", result)

            function_responses.append(
                types.Part.from_function_response(
                    name = call.name,
                    response = result
                )
            )

        # send function results back to Gemini
        contents.append(
            types.Content(
                role = "user",
                parts = function_responses
            )
        )