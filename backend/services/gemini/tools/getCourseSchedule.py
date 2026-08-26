import json


# get data from json
with open("data/courseScheduleData.json", "r") as file:
    course_schedule_data = json.load(file)


# tool function
def get_course_schedule(
    course_id=None
):
    """
    Returns schedule of one of the student's classes
    """

    schedule = course_schedule_data.get("schedule")

    # if no schedule data, call error
    if not schedule:
        return {
            "error": f"I don't have any course schedule data."
        }

    # if a course_id was provided, find that specific course
    if course_id:
        for course in schedule:
            if course["course_id"] == course_id:
                return course

        return {
            "error": f"I don't have schedule data for course {course_id}."
        }

    # otherwise return all schedules
    return schedule


# Gemini tool declaration
get_course_schedule_tool = {
    "name": "get_course_schedule",
    "description": "Gets the class schedule for a specific course.",
    "parameters": {
        "type": "object",
        "properties": {
            "course_id": {
                "type": "string",
                "description": "The Canvas course ID, such as COP4600."
            }
        },
        "required": []
    }
}
