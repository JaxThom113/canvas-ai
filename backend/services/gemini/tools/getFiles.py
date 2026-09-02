# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_files(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None,
    course_id = None
):
    """
    Returns all files for a class.
    """

    return None


# Gemini tool declaration
get_files_tool = {
    "name": "get_files",
    "description": "Gets all the files in a class.",
    "parameters": {
        "type": "object",
        "properties": {
            "course_id": {
                "type": "string",
                "description": "The Canvas course ID to filter by, such as COP4600."
            }
        },
        "required": []
    }
}
