# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_upcoming_events(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None
):
    """
    Returns the student's list of upcoming events.
    """

    if not base_url:
        return {
            "error": "No Canvas base URL was provided."
        }

    # build the full Canvas endpoint
    endpoint = (
        f"{base_url.rstrip('/')}"
        "/api/v1/users/self/upcoming_events"
    )

    try:
        # call Canvas API (using my backend function)
        upcoming_events = access_canvas(endpoint, cookies)
    
    except (RuntimeError, ValueError) as error:
        return {
            "error": f"Could not fetch upcoming_events from Canvas: {error}"
        }

    if not upcoming_events:
        return {
            "error": "I don't have any upcoming_events data."
        }

    return upcoming_events


# Gemini tool declaration
get_upcoming_events_tool = {
    "name": "get_upcoming_events",
    "description": "Gets the list of upcoming events for the user.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}
