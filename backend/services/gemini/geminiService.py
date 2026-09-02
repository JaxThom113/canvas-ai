import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors

# import tools
from services.gemini.tools.getAnnouncements import get_announcements
from services.gemini.tools.getAssignments import get_assignments
from services.gemini.tools.getCalendarEvents import get_calendar_events
from services.gemini.tools.getCourseDetails import get_course_details
from services.gemini.tools.getCourses import get_courses
from services.gemini.tools.getCourseSchedule import get_course_schedule

from services.gemini.tools.getAnnouncements import get_announcements_tool
from services.gemini.tools.getAssignments import get_assignments_tool
from services.gemini.tools.getCalendarEvents import get_calendar_events_tool
from services.gemini.tools.getCourseDetails import get_course_details_tool
from services.gemini.tools.getCourses import get_courses_tool
from services.gemini.tools.getCourseSchedule import get_course_schedule_tool

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
                                    get_calendar_events_tool,
                                    get_course_details_tool,
                                    get_courses_tool,
                                    get_course_schedule_tool
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

            print(f"Gemini called {call.name}")
            print("Arguments:", call.args)

            # select the right tool function
            match call.name:

                case "get_announcements":
                    result = get_announcements(
                        call.args.get("course_id"),
                        call.args.get("start_date"),
                        call.args.get("end_date"),
                        call.args.get("important_only", False),
                    )

                case "get_assignments":
                    result = get_assignments(
                        call.args.get("course_id"),
                        call.args.get("start_date"),
                        call.args.get("end_date"),
                        call.args.get("include_completed", False),
                    )

                case "get_calendar_events": 
                    result = get_calendar_events(
                        call.args["start_date"],
                        call.args["end_date"],
                    )

                case "get_course_details": 
                    result = get_course_details(
                        call.args["course_id"]
                    )

                case "get_courses": 
                    result = get_courses()

                case "get_course_schedule":
                    result = get_course_schedule(
                        call.args.get("course_id")
                    )
                    
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