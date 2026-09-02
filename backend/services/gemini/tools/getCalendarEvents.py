# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_calendar_events(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None,
    start_date = None,
    end_date = None
):
    """
    Returns all calendar events in a specified date range.
    """

    return None


# Gemini tool declaration
get_calendar_events_tool = {
    "name": "get_calendar_events",
    "description": "Gets all the calendar events in a specified date range.",
    "parameters": {
        "type": "object",
        "properties": {
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
