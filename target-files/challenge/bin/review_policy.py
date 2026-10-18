#!/usr/bin/env python3
"""BlackTrace BT-204 review policy."""

ALLOWED_TICKETS = {"BT-204"}
ALLOWED_ACTIONS = {"review", "status-check", "profile-check"}
REQUIRED_REVIEWER = "maintenance-operator"
REQUIRED_PROFILE = "NIGHTJAR-17"


def validate_request(request):
    if not isinstance(request, dict):
        return False, "request must be an object"

    ticket = request.get("ticket")
    action = request.get("action")
    reviewer = request.get("reviewer")

    if ticket not in ALLOWED_TICKETS:
        return False, "unknown ticket"

    if action not in ALLOWED_ACTIONS:
        return False, "unsupported action"

    if reviewer != REQUIRED_REVIEWER:
        return False, "reviewer is not authorized"

    if action == "profile-check":
        if request.get("profile") != REQUIRED_PROFILE:
            return False, "workflow profile is not authorized"

    return True, "request accepted"
