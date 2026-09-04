# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_files(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None,
    id = None
):
    """
    Returns all files for a class.
    """

    if not base_url:
        return {
            "error": "No Canvas base URL was provided."
        }

    # build the full Canvas endpoint
    endpoint = (
        f"{base_url.rstrip('/')}"
        f"/api/v1/courses/{id}/files"
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
get_files_tool = {
    "name": "get_files",
    "description": "Gets all the files in a class.",
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
