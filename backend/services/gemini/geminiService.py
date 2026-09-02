import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors

# import tools
from services.gemini.tools.getCourses import get_courses
from services.gemini.tools.getTodo import get_todo
from services.gemini.tools.getUpcomingEvents import get_upcoming_events

from services.gemini.tools.getCourses import get_courses_tool
from services.gemini.tools.getTodo import get_todo_tool
from services.gemini.tools.getUpcomingEvents import get_upcoming_events_tool

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.5-flash-lite"


# main Gemini prompting function
def ask_gemini(prompt: str, base_url: str | None = None, cookies: dict[str, str] | None = None):

    contents = [
        types.Content(
            role = "user",
            parts = [
                types.Part.from_text(text=prompt)
            ]
        )
    ]

    while True:

        # try contacting Gemini 3 times
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model = MODEL,
                    contents = contents,
                    config = types.GenerateContentConfig(
                        tools = [
                            types.Tool(
                                function_declarations = [
                                    get_courses_tool,
                                    get_todo_tool,
                                    get_upcoming_events_tool
                                ]
                            )
                        ]
                    )
                )
                break
            except errors.ServerError as e:
                # 503 error means Gemini is overloaded - wait and retry
                if e.code == 503 and attempt < 2:
                    time.sleep(2 ** attempt)  # 1s, then 2s
                    continue
                raise

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

            # log what tool functions Gemini calls and what parameters it uses 
            print("Gemini called:", call.name)
            print("Arguments:", call.args)

            # select the right tool function
            match call.name:

                case "get_courses":
                    result = get_courses(base_url, cookies)

                case "get_todo":
                    result = get_todo(base_url, cookies)

                case "get_upcoming_events":
                    result = get_upcoming_events(base_url, cookies)
                    
                case _: 
                    result = { "error": f"Unknown function: {call.name}" }

            print("Function result:", result)

            function_responses.append(
                types.Part.from_function_response(
                    name = call.name,
                    response = result if isinstance(result, dict) else {"result": result}
                )
            )

        # send function results back to Gemini
        contents.append(
            types.Content(
                role = "user",
                parts = function_responses
            )
        )