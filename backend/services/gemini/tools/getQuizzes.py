# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_quizzes(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None,
    id = None
):
    """
    Returns all quizzes for a class.
    """

    if not base_url:
        return {
            "error": "No Canvas base URL was provided."
        }

    # build the full Canvas endpoint
    endpoint = (
        f"{base_url.rstrip('/')}"
        f"/api/v1/courses/{id}/quizzes"
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

    return result


# Gemini tool declaration
get_quizzes_tool = {
    "name": "get_quizzes",
    "description": "Gets all the quizzes in a class.",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The 7-digit id number for a class seen when accessing the /api/v1/users/self/courses Canvas API endpoint."
            }
        },
        "required": []
    }
}
