import json
from datetime import datetime


# get data from json
with open("data/calendarEventsData.json", "r") as file:
    calendar_events_data = json.load(file)


# tool function
def get_calendar_events(
    start_date: str,
    end_date: str
):
    """
    Returns calendar events within a specified start and end date.
    """

    # convert the input string timestamps into datetime objects
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    matching_events = []

    # build a list of events in the json within the start/end window
    for event in calendar_events_data.values():
        event_start = datetime.fromisoformat(event["start"])
        if start <= event_start <= end:
            matching_events.append(event)

    # no events found
    if not matching_events:
        return {
            "message": f"No calendar events found within the specified {start_date} - {end_date} date range."
        }

    # return list of found events
    return matching_events


# Gemini tool declaration
get_calendar_events_tool = {
    "name": "get_calendar_events",
    "description": "Gets the calendar events for all courses between a specified start and end date.",
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
            }
        },
        "required": ["start_date", "end_date"]
    }
}
