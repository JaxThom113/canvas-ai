# import the Canvas API client
from services.canvas.canvasService import access_canvas
from services.canvas.canvasJsonParser import parse_canvas_json


# tool function
def get_courses(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None
):
    """
    Returns all courses the student is currently enrolled in.
    """

    if not base_url:
        return {
            "error": "No Canvas base URL was provided."
        }

    # build the full Canvas endpoint
    endpoint = (
        f"{base_url.rstrip('/')}"
        "/api/v1/users/self/courses?enrollment_state=active&per_page=100"
    )

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

    # trim the raw Canvas JSON down to what NaviGator needs
    return parse_canvas_json("courses", result)


# tool declaration
get_courses_tool = {
    "name": "get_courses",
    "description": "Gets all the courses the user is enrolled in.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}
