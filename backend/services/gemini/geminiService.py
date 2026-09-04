import os
import time
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors

# import tools
from services.gemini.tools.getAnnouncements import get_announcements, get_announcements_tool
from services.gemini.tools.getAssignments import get_assignments, get_assignments_tool
from services.gemini.tools.getCourses import get_courses, get_courses_tool
from services.gemini.tools.getDiscussions import get_discussions, get_discussions_tool
from services.gemini.tools.getFiles import get_files, get_files_tool
from services.gemini.tools.getGrades import get_grades, get_grades_tool
from services.gemini.tools.getModules import get_modules, get_modules_tool
from services.gemini.tools.getQuizzes import get_quizzes, get_quizzes_tool
from services.gemini.tools.getTodo import get_todo, get_todo_tool
from services.gemini.tools.getUpcomingEvents import get_upcoming_events, get_upcoming_events_tool


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.5-flash-lite"
MAX_DISPLAY_CHARS = 10000


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
                                    get_announcements_tool,
                                    get_assignments_tool,
                                    get_courses_tool,
                                    get_discussions_tool,
                                    get_files_tool,
                                    get_grades_tool,
                                    get_modules_tool,
                                    get_quizzes_tool,
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

            called_function_debug(call.name)
            arguments_debug(call.args)
            
            # select the right tool function
            match call.name:

                case "get_announcements":
                    result = get_announcements(base_url, cookies, call.args["id"], call.args["start_date"], call.args["end_date"])

                case "get_assignments":
                    result = get_assignments(base_url, cookies, call.args["id"], call.args["start_date"], call.args["end_date"])

                case "get_courses":
                    result = get_courses(base_url, cookies)

                case "get_discussions":
                    result = get_discussions(base_url, cookies, call.args["id"])

                case "get_files":
                    result = get_files(base_url, cookies, call.args["id"])

                case "get_grades":
                    result = get_grades(base_url, cookies, call.args["id"])

                case "get_modules":
                    result = get_modules(base_url, cookies, call.args["id"])

                case "get_quizzes":
                    result = get_quizzes(base_url, cookies, call.args["id"])

                case "get_todo":
                    result = get_todo(base_url, cookies)

                case "get_upcoming_events":
                    result = get_upcoming_events(base_url, cookies)
                    
                case _: 
                    result = { "error": f"Unknown function: {call.name}" }

            function_result_debug(result)

            # add resulting json to list of tool function responses to give to the agent
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


def called_function_debug(name):
    # log what tool function Gemini calls
    print("==================================================")
    print("Gemini called:", f"\033[92m{name}\033[0m")


def arguments_debug(args):
    # log  arguments passed in by Gemini, limit max characters printed
    print("\nArguments:")

    arg_chars = len(args)

    if arg_chars > MAX_DISPLAY_CHARS:
        print(f"\033[93m(truncated, {arg_chars} chars)\033[0m")
    else:
        print(f"\033[96m({arg_chars} chars)\033[0m")
        print(json.dumps(args, indent=2))


def function_result_debug(result):
    # log resulting json
    print("\nTool function result:")

    result_chars = sum(len(str(item)) for item in result)

    if result_chars > MAX_DISPLAY_CHARS:
        print(f"\033[93m(truncated, {result_chars} chars)\033[0m")
    else:
        print(f"\033[96m({result_chars} chars)\033[0m")
        print(json.dumps(result, indent=2))