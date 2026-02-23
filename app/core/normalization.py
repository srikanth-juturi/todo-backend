import re

DEFAULT_CATEGORY = "general"
_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_single_line_whitespace(value: str) -> str:
    return _WHITESPACE_PATTERN.sub(" ", value.strip())


def normalize_title(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("Title must be a string")

    normalized_value = normalize_single_line_whitespace(value)
    if not normalized_value:
        raise ValueError("Title must not be empty")
    if len(normalized_value) > 200:
        raise ValueError("Title must be at most 200 characters")
    return normalized_value


def normalize_category(
    value: object | None,
    *,
    default_if_empty: bool,
    coerce_numeric: bool,
) -> str:
    if value is None:
        if default_if_empty:
            return DEFAULT_CATEGORY
        raise ValueError("Category must not be empty")

    if coerce_numeric and isinstance(value, (int, float)) and not isinstance(value, bool):
        value = str(value)

    if not isinstance(value, str):
        raise TypeError("Category must be a string")

    normalized_value = normalize_single_line_whitespace(value)
    if not normalized_value:
        if default_if_empty:
            return DEFAULT_CATEGORY
        raise ValueError("Category must not be empty")

    if len(normalized_value) > 50:
        raise ValueError("Category must be at most 50 characters")
    return normalized_value


def canonicalize_text(value: str) -> str:
    return normalize_single_line_whitespace(value).casefold()