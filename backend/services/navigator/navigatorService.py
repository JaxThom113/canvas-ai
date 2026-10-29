import os
import time
import json

from dotenv import load_dotenv
from openai import OpenAI, APIStatusError

# import tools
from services.navigator.tools.getAnnouncements import get_announcements, get_announcements_tool
from services.navigator.tools.getAssignments import get_assignments, get_assignments_tool
from services.navigator.tools.getCourses import get_courses, get_courses_tool
from services.navigator.tools.getDiscussions import get_discussions, get_discussions_tool
from services.navigator.tools.getFiles import get_files, get_files_tool
from services.navigator.tools.getGrades import get_grades, get_grades_tool
from services.navigator.tools.getModules import get_modules, get_modules_tool
from services.navigator.tools.getQuizzes import get_quizzes, get_quizzes_tool
from services.navigator.tools.getTodo import get_todo, get_todo_tool
from services.navigator.tools.getUpcomingEvents import get_upcoming_events, get_upcoming_events_tool


load_dotenv()
client = OpenAI(
    api_key = os.getenv("NAVIGATOR_API_KEY"),
    base_url = os.getenv("NAVIGATOR_BASE_URL")
)

MODEL = os.getenv("NAVIGATOR_MODEL")
MAX_DISPLAY_CHARS = 10000

# wrap each tool declaration in the OpenAI-style function format
TOOLS = [
    {"type": "function", "function": tool}
    for tool in [
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
]


# main NaviGator prompting function
def ask_navigator(prompt: str, base_url: str | None = None, cookies: dict[str, str] | None = None):

    messages = [
        {"role": "user", "content": prompt}
    ]

    while True:

        # try contacting NaviGator 3 times
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model = MODEL,
                    messages = messages,
                    tools = TOOLS
                )
                break
            except APIStatusError as e:
                # 503 / 429 means the server is overloaded - wait and retry
                if e.status_code in (429, 503) and attempt < 2:
                    time.sleep(2 ** attempt)  # 1s, then 2s
                    continue
                raise

        message = response.choices[0].message

        # preserve the model's response
        messages.append(message)

        # if no function calls required, return
        if not message.tool_calls:
            return message.content

        # execute functions
        for call in message.tool_calls:

            name = call.function.name

            # arguments arrive as a JSON string
            try:
                args = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}

            called_function_debug(name)
            arguments_debug(args)

            # select the right tool function
            match name:

                case "get_announcements":
                    result = get_announcements(base_url, cookies, args.get("id"), args.get("start_date"), args.get("end_date"))

                case "get_assignments":
                    result = get_assignments(base_url, cookies, args.get("id"), args.get("start_date"), args.get("end_date"))

                case "get_courses":
                    result = get_courses(base_url, cookies)

                case "get_discussions":
                    result = get_discussions(base_url, cookies, args.get("id"))

                case "get_files":
                    result = get_files(base_url, cookies, args.get("id"))

                case "get_grades":
                    result = get_grades(base_url, cookies, args.get("id"))

                case "get_modules":
                    result = get_modules(base_url, cookies, args.get("id"))

                case "get_quizzes":
                    result = get_quizzes(base_url, cookies, args.get("id"))

                case "get_todo":
                    result = get_todo(base_url, cookies)

                case "get_upcoming_events":
                    result = get_upcoming_events(base_url, cookies)

                case _:
                    result = { "error": f"Unknown function: {name}" }

            function_result_debug(result)

            # send each tool function result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, default=str)
            })

        print("==================================================")


def called_function_debug(name):
    # log what tool function the model calls
    print("==================================================")
    print("NaviGator called:", f"\033[92m{name}\033[0m")


def arguments_debug(args):
    # log  arguments passed in by the model, limit max characters printed
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