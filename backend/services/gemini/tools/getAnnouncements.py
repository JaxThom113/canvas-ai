from urllib.parse import urlencode

# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_announcements(
    base_url: str | None = None,
    cookies: dict[str, str] | None = None,
    id = None,
    start_date = None,
    end_date = None
):
    """
    Returns all announcements for a class in a specified date range.
    """

    if not base_url:
        return {
            "error": "No Canvas base URL was provided."
        }

    # start with the required course filter, add dates only if provided
    params = [("context_codes[]", f"course_{id}")]
    if start_date:
        params.append(("start_date", start_date))
    if end_date:
        params.append(("end_date", end_date))

    # build the full Canvas endpoint
    endpoint = f"{base_url.rstrip('/')}/api/v1/announcements?{urlencode(params)}"

    try:
        # call Canvas API (using my backend function)
        result = access_canvas(endpoint, cookies)
    
    except (RuntimeError, ValueError) as error:
        return {
            "error": f"Could not fetch from Canvas: {error}"
        }

    if not result:
        return {
            "error": "No data was provided."
        }

    return result


# Gemini tool declaration
get_announcements_tool = {
    "name": "get_announcements",
    "description": "Gets all the announcements in a class in a specified date range.",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The 7-digit id number for a class seen when accessing the /api/v1/users/self/courses Canvas API endpoint."
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
