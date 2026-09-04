from datetime import datetime, timezone

# import the Canvas API client
from services.canvas.canvasService import access_canvas


def _to_dt(value):
    # Canvas returns UTC like "2026-08-30T23:59:59Z"; the agent may send naive ISO.
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))

    # make naive input comparable
    if dt.tzinfo is None: 
        dt = dt.replace(tzinfo=timezone.utc)

    return dt


# tool function
def get_assignments(
    base_url: str | None = None,
    cookies: dict[str, str] | None = None,
    id = None,
    start_date = None,
    end_date = None
):
    """
    Returns all assignments for a class in a specified date range.
    """

    if not base_url:
        return {
            "error": "No Canvas base URL was provided."
        }

    # build the full Canvas endpoint
    endpoint = (
        f"{base_url.rstrip('/')}"
        f"/api/v1/courses/{id}/assignments?per_page=100"
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

    # filter locally by due date, only if a range was given
    if start_date or end_date:
        start = None
        if start_date:
            start = _to_dt(start_date)

        end = None
        if end_date:
            end = _to_dt(end_date)

        filtered = []
        for assignment in result:
            due = assignment.get("due_at")

            # skip assignments with no due date
            if not due:
                continue  

            due_dt = _to_dt(due)

            # skip if outside of date bounds
            if start and due_dt < start:
                continue
            if end and due_dt > end:
                continue

            filtered.append(assignment)

        result = filtered

    return result


# Gemini tool declaration
get_assignments_tool = {
    "name": "get_assignments",
    "description": "Gets all the assignments in a class in a specified date range.",
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
