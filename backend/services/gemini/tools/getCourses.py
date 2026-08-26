import json


# get data from json
with open("data/courseData.json", "r") as file:
    course_data = json.load(file)


# tool function
def get_courses():
    """
    Returns all courses the student is currently enrolled in.
    """

    # get all course data
    courses = course_data.get("courses")
    
    if not courses:
        return {
            "error": f"I don't have any course data."
        }

    return courses


# Gemini tool declaration
get_courses_tool = {
    "name": "get_courses",
    "description": "Gets all the courses the user is enrolled in.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}
