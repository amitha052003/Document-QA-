
def validate_question(question: str):
    """
    Validate the user's question.
    """

    if not question or not question.strip():
        return False, "Please enter a question."

    question = question.strip()

    if len(question) < 3:
        return False, "Please enter a more detailed question."

    if len(question) > 1000:
        return False, "Question is too long. Please keep it under 1000 characters."

    return True, ""


def check_prompt_injection(question: str):
    """
    Check for common prompt injection attempts.
    """

    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore your instructions",
        "forget previous instructions",
        "system prompt",
        "reveal your prompt",
        "show me your prompt",
        "developer message",
        "bypass your instructions",
        "jailbreak"
    ]

    question_lower = question.lower()

    for pattern in suspicious_patterns:
        if pattern in question_lower:
            return False

    return True

