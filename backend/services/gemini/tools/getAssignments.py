import json
from datetime import datetime


# get data from json
with open("data/assignmentsData.json", "r") as file:
    assignments_data = json.load(file)


# tool function
def get_assignments(
    course_id=None,
    start_date=None,
    end_date=None,
    include_completed=False
):
    """
    Gets assignments due within a specified date range, optionally filters 
    assignments by course and completion status.
    """

    assignments = assignments_data.get("assignments", [])

    if not assignments:
        return {
            "error": "I don't have any assignment data."
        }

    # convert dates if provided
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None

    matching_assignments = []

    for assignment in assignments:

        # filter by course if a course_id was provided
        if course_id and assignment["course_id"] != course_id:
            continue

        # filter completed assignments
        if not include_completed and assignment["status"] == "completed":
            continue

        # filter by due date
        due_date = datetime.fromisoformat(assignment["due_date"])

        if start and due_date < start:
            continue

        if end and due_date > end:
            continue

        matching_assignments.append(assignment)

    # no assignments found
    if not matching_assignments:
        return {
            "message": "No assignments found matching the specified criteria."
        }

    return matching_assignments


# Gemini tool declaration
get_assignments_tool = {
    "name": "get_assignments",
    "description": "Gets assignments due within a specified date range. Can optionally filter assignments by course and completion status.",
    "parameters": {
        "type": "object",
        "properties": {
            "course_id": {
                "type": "string",
                "description": "The Canvas course ID to filter by, such as COP4600. If omitted, assignments from all courses are returned."
            },
            "start_date": {
                "type": "string",
                "description": "The beginning of the date range in ISO 8601 format, such as 2026-08-24T00:00:00."
            },
            "end_date": {
                "type": "string",
                "description": "The end of the date range in ISO 8601 format, such as 2026-08-30T23:59:59."
            },
            "include_completed": {
                "type": "boolean",
                "description": "Whether to include assignments that have already been completed."
            }
        },
        "required": []
    }
}
