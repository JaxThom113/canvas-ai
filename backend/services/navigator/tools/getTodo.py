# import the Canvas API client
from services.canvas.canvasService import access_canvas
from services.canvas.canvasJsonParser import parse_canvas_json


# tool function
def get_todo(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None
):
    """
    Returns the student's todo list.
    """

    if not base_url:
        return {
            "error": "No Canvas base URL was provided."
        }

    # build the full Canvas endpoint
    endpoint = (
        f"{base_url.rstrip('/')}"
        "/api/v1/users/self/todo"
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
    return parse_canvas_json("todo", result)


# tool declaration
get_todo_tool = {
    "name": "get_todo",
    "description": "Gets the todo list of the user.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}
