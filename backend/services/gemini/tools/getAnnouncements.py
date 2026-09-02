# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_announcements(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None,
    course_id = None,
    start_date = None,
    end_date = None
):
    """
    Returns all announcements for a class in a specified date range.
    """

    return None


# Gemini tool declaration
get_announcements_tool = {
    "name": "get_announcements",
    "description": "Gets all the announcements in a class in a specified date range.",
    "parameters": {
        "type": "object",
        "properties": {
            "course_id": {
                "type": "string",
                "description": "The Canvas course ID to filter by, such as COP4600."
            },
            "start_date": {
                "type": "string",
                "description": "The beginning of the date range in ISO 8601 format, such as 2026-08-24T00:00:00."
            },
            "end_date": {
                "type": "string",
                "description": "The end of the date range in ISO 8601 format, such as 2026-08-30T23:59:59."
            },
        },
        "required": []
    }
}
