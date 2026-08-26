import json


# get data from json
with open("data/courseDetailsData.json", "r") as file:
    course_details_data = json.load(file)


# tool function
def get_course_details(
    course_id: str
):
    """
    Returns details of one of the student's classes
    """

    # get details of a specifid course
    details = course_details_data.get(course_id)

    if not details:
        return {
            "error": f"I don't have details for {course_id}."
        }

    return details


# Gemini tool declaration
get_course_details_tool = {
    "name": "get_course_details",
    "description": "Gets the details and important information for a specific course.",
    "parameters": {
        "type": "object",
        "properties": {
            "course_id": {
                "type": "string",
                "description": "The Canvas course ID, such as COP4600."
            }
        },
        "required": ["course_id"]
    }
}
