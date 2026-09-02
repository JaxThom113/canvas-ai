# import the Canvas API client
from services.canvas.canvasService import access_canvas


# tool function
def get_quizzes(
    base_url: str | None = None, 
    cookies: dict[str, str] | None = None,
    course_id = None
):
    """
    Returns all quizzes for a class.
    """

    return None


# Gemini tool declaration
get_quizzes_tool = {
    "name": "get_quizzes",
    "description": "Gets all the quizzes in a class.",
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
