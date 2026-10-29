from typing import Any, Callable

from services.canvas.canvasHtmlParser import html_to_text, MESSAGE_LIMIT


def compact(data: dict[str, Any]) -> dict[str, Any]:
    # keys that are None or empty don't have meaning, so remove them
    # however, keep false and 0 because they are meaningful
    return {
        key: value
        for key, value in data.items()
        if value is not None and value != "" and value != [] and value != {}
    }


def human_size(size: int | None) -> str | None:
    if size is None:
        return None

    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024


def author_name(item: dict[str, Any]) -> str | None:
    author = item.get("author") or {}
    return author.get("display_name") or item.get("user_name")


def parse_submission(submission: dict[str, Any] | None) -> dict[str, Any] | None:
    # only present when the endpoint is called with include[]=submission
    if not submission:
        return None

    return compact({
        "status": submission.get("workflow_state"),
        "submitted_at": submission.get("submitted_at"),
        "score": submission.get("score"),
        "grade": submission.get("grade"),
        "late": submission.get("late") or None,
        "missing": submission.get("missing") or None,
        "excused": submission.get("excused") or None,
    })


def parse_announcement(announcement: dict[str, Any]) -> dict[str, Any]:
    return compact({
        "id": announcement.get("id"),
        "title": announcement.get("title"),
        "course": announcement.get("context_code"),
        "posted_at": announcement.get("posted_at"),
        "author": author_name(announcement),
        "message": html_to_text(announcement.get("message"), MESSAGE_LIMIT),
        "html_url": announcement.get("html_url"),
    })


def parse_assignment(assignment: dict[str, Any]) -> dict[str, Any]:
    attempts = assignment.get("allowed_attempts")

    return compact({
        "id": assignment.get("id"),
        "name": assignment.get("name"),
        "course_id": assignment.get("course_id"),
        "due_at": assignment.get("due_at"),
        "unlock_at": assignment.get("unlock_at"),
        "lock_at": assignment.get("lock_at"),
        "points_possible": assignment.get("points_possible"),
        "grading_type": assignment.get("grading_type"),
        "submission_types": assignment.get("submission_types"),
        "allowed_extensions": assignment.get("allowed_extensions"),
        "allowed_attempts": attempts if attempts and attempts > 0 else None,
        "is_quiz": assignment.get("is_quiz_assignment") or None,
        "locked": assignment.get("locked_for_user"),
        "lock_explanation": assignment.get("lock_explanation"),
        "submission": parse_submission(assignment.get("submission")),
        "description": html_to_text(assignment.get("description")),
        "html_url": assignment.get("html_url"),
    })


def parse_course(course: dict[str, Any]) -> dict[str, Any] | None:
    # courses the user can no longer open only contain an id, skip them
    if course.get("access_restricted_by_date") or not course.get("name"):
        return None

    enrollments = course.get("enrollments") or []

    return compact({
        "id": course.get("id"),
        "name": course.get("name"),
        "course_code": course.get("course_code"),
        "term_id": course.get("enrollment_term_id"),
        "term": (course.get("term") or {}).get("name"),
        "start_at": course.get("start_at"),
        "end_at": course.get("end_at"),
        "role": enrollments[0].get("type") if enrollments else None,
        "current_score": enrollments[0].get("computed_current_score") if enrollments else None,
        "current_grade": enrollments[0].get("computed_current_grade") if enrollments else None,
    })


def parse_discussion(discussion: dict[str, Any]) -> dict[str, Any]:
    # graded discussions carry their due date on the nested assignment
    assignment = discussion.get("assignment") or {}

    return compact({
        "id": discussion.get("id"),
        "title": discussion.get("title"),
        "posted_at": discussion.get("posted_at"),
        "last_reply_at": discussion.get("last_reply_at"),
        "author": author_name(discussion),
        "reply_count": discussion.get("discussion_subentry_count"),
        "unread_count": discussion.get("unread_count") or None,
        "due_at": assignment.get("due_at"),
        "points_possible": assignment.get("points_possible"),
        "todo_date": discussion.get("todo_date"),
        "lock_at": discussion.get("lock_at"),
        "locked": discussion.get("locked_for_user"),
        "message": html_to_text(discussion.get("message"), MESSAGE_LIMIT),
        "html_url": discussion.get("html_url"),
    })


def parse_file(file: dict[str, Any]) -> dict[str, Any]:
    return compact({
        "id": file.get("id"),
        "name": file.get("display_name") or file.get("filename"),
        "type": file.get("content-type") or file.get("mime_class"),
        "size": human_size(file.get("size")),
        "updated_at": file.get("updated_at"),
        "locked": file.get("locked_for_user"),
        "url": file.get("url"),
    })


def parse_enrollment(enrollment: dict[str, Any]) -> dict[str, Any] | None:
    grades = enrollment.get("grades") or {}

    # roster entries without grades (other users, teachers) are not useful here
    if not grades:
        return None

    return compact({
        "course_id": enrollment.get("course_id"),
        "type": enrollment.get("type"),
        "current_score": grades.get("current_score"),
        "current_grade": grades.get("current_grade"),
        "final_score": grades.get("final_score"),
        "final_grade": grades.get("final_grade"),
        "html_url": grades.get("html_url"),
    })


def parse_module_item(item: dict[str, Any]) -> dict[str, Any]:
    requirement = item.get("completion_requirement") or {}

    return compact({
        "title": item.get("title"),
        "type": item.get("type"),
        "requirement": requirement.get("type"),
        "completed": requirement.get("completed"),
        "html_url": item.get("html_url"),
    })


def parse_module(module: dict[str, Any]) -> dict[str, Any]:
    items = module.get("items")

    return compact({
        "id": module.get("id"),
        "name": module.get("name"),
        "position": module.get("position"),
        "unlock_at": module.get("unlock_at"),
        "state": module.get("state"),
        "completed_at": module.get("completed_at"),
        "items_count": module.get("items_count"),
        "items": [parse_module_item(item) for item in items] if items else None,
    })


def parse_quiz(quiz: dict[str, Any]) -> dict[str, Any]:
    attempts = quiz.get("allowed_attempts")

    return compact({
        "id": quiz.get("id"),
        "title": quiz.get("title"),
        "quiz_type": quiz.get("quiz_type"),
        "due_at": quiz.get("due_at"),
        "unlock_at": quiz.get("unlock_at"),
        "lock_at": quiz.get("lock_at"),
        "points_possible": quiz.get("points_possible"),
        "question_count": quiz.get("question_count"),
        "time_limit_minutes": quiz.get("time_limit"),
        "allowed_attempts": attempts if attempts and attempts > 0 else None,
        "locked": quiz.get("locked_for_user"),
        "lock_explanation": quiz.get("lock_explanation"),
        "description": html_to_text(quiz.get("description")),
        "html_url": quiz.get("html_url"),
    })


def parse_todo_item(item: dict[str, Any]) -> dict[str, Any]:
    assignment = item.get("assignment") or item.get("quiz") or {}

    return compact({
        "type": item.get("type"),
        "course_id": item.get("course_id"),
        "name": assignment.get("name") or assignment.get("title"),
        "due_at": assignment.get("due_at"),
        "points_possible": assignment.get("points_possible"),
        "submission_types": assignment.get("submission_types"),
        "html_url": item.get("html_url") or assignment.get("html_url"),
    })


def parse_upcoming_event(event: dict[str, Any]) -> dict[str, Any]:
    assignment = event.get("assignment") or {}

    return compact({
        "title": event.get("title"),
        "type": event.get("type"),
        "course": event.get("context_name") or event.get("context_code"),
        "start_at": event.get("start_at"),
        "end_at": event.get("end_at"),
        "all_day": event.get("all_day") or None,
        "location": event.get("location_name"),
        "due_at": assignment.get("due_at"),
        "points_possible": assignment.get("points_possible"),
        "description": html_to_text(event.get("description"), MESSAGE_LIMIT),
        "html_url": event.get("html_url"),
    })


# maps a resource name to the parser for one of its objects
PARSERS: dict[str, Callable[[dict[str, Any]], dict[str, Any] | None]] = {
    "courses": parse_course,
    "assignments": parse_assignment,
    "announcements": parse_announcement,
    "discussions": parse_discussion,
    "files": parse_file,
    "grades": parse_enrollment,
    "modules": parse_module,
    "quizzes": parse_quiz,
    "todo": parse_todo_item,
    "upcoming_events": parse_upcoming_event,
}


# main function for parsing JSON data
def parse_canvas_json(resource: str, data: Any) -> Any:
    """
    Trims a raw Canvas API response for the given resource type (i.e. announcements, discussions).
    """

    parser = PARSERS.get(resource)

    # unknown resource, nothing to trim
    if parser is None:
        return data

    if isinstance(data, list):
        parsed = [parser(item) for item in data if isinstance(item, dict)]
        return [item for item in parsed if item]

    if isinstance(data, dict):
        # leave our own errors and Canvas error payloads alone
        if "error" in data or "errors" in data:
            return data
        return parser(data) or {}

    return data
