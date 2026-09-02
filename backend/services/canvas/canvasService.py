import json
from typing import Any
from urllib import error, request

# import JSON parser
from services.canvas.canvasJsonParser import parse_canvas_json


# main function for interfacing with Canvas API
def access_canvas(endpoint: str, cookies: dict[str, str] | None = None) -> Any:
    """
    Fetch a Canvas API URL using the active browser session cookies
    """

    # ensure endpoint given from frontend is not empty
    if not endpoint or not endpoint.strip():
        raise ValueError("A Canvas endpoint must be provided.")

    parse_canvas_json()

    # tell Canvas a JSON is needed as response
    headers = {
        "Accept": "application/json",
    }

    # if cookies are given, convert JSON into single cookie header string
    if cookies:
        cookie_header = "; ".join(f"{key}={value}" for key, value in cookies.items())
        headers["Cookie"] = cookie_header

    # setup the API request
    req = request.Request(endpoint.strip(), headers=headers, method="GET")

    try:
        # send the API request to Canvas
        with request.urlopen(req, timeout=30) as response:
            # read response
            body = response.read().decode("utf-8")

            # if empty, return empty dictionary
            if not body:
                return {}
            
            return json.loads(body)
        
    except error.HTTPError as exc:
        # catch 401, 403, 404 errors
        payload = exc.read().decode("utf-8", errors="replace")
        message = payload or f"Canvas request failed with status {exc.code}."
        raise RuntimeError(message) from exc
    
    except Exception as exc:
        # catch all other exceptions
        raise RuntimeError(f"Unable to reach Canvas API: {exc}") from exc
