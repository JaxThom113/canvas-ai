import json
from datetime import datetime


# get data from json
with open("data/announcementsData.json", "r") as file:
    announcements_data = json.load(file)


# tool function
def get_announcements(
    course_id=None,
    start_date=None,
    end_date=None,
    important_only=False
):
    """
    Gets announcements made within a specified date range, optionally filters 
    announcements by course and importance.
    """

    announcements = announcements_data.get("announcements", [])

    if not announcements:
        return {
            "error": "I don't have any announcement data."
        }

    # Convert dates if provided
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None

    matching_announcements = []

    for announcement in announcements:

        # filter by course if a course_id was provided
        if course_id and announcement["course_id"] != course_id:
            continue

        # filter important announcements if requested
        if important_only and not announcement["important"]:
            continue

        # filter by posted date
        posted_at = datetime.fromisoformat(announcement["posted_at"])

        if start and posted_at < start:
            continue

        if end and posted_at > end:
            continue

        matching_announcements.append(announcement)

    # no announcements found
    if not matching_announcements:
        return {
            "message": "No announcements found matching the specified criteria."
        }

    return matching_announcements


# Gemini tool declaration
get_announcements_tool = {
    "name": "get_announcements",
    "description": "Gets announcements posted within a specified date range. Can optionally filter announcements by course and importance.",
    "parameters": {
        "type": "object",
        "properties": {
            "course_id": {
                "type": "string",
                "description": "The Canvas course ID to filter by, such as COP4600. If omitted, announcements from all courses are returned."
            },
            "start_date": {
                "type": "string",
                "description": "The beginning of the date range in ISO 8601 format, such as 2026-08-24T00:00:00."
            },
            "end_date": {
                "type": "string",
                "description": "The end of the date range in ISO 8601 format, such as 2026-08-30T23:59:59."
            },
            "important_only": {
                "type": "boolean",
                "description": "Whether to return only announcements marked as important."
            }
        },
        "required": []
    }
}
