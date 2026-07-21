"""
Lightweight, rule-based "AI" natural-language search parser.

This is intentionally simple and dependency-free so the platform works
out of the box. It's the seed for the real AI Smart Search feature —
swap `parse_natural_query` internals for a call to an LLM (e.g. the
Anthropic API) once you're ready, keeping the same return shape so
nothing else in the app has to change.

Example:
    parse_natural_query("black Mercedes G63 under $170,000")
    -> {"make": "Mercedes", "model": "G63", "price_max": 170000,
        "exterior_color": "black"}
"""

import re

COMMON_MAKES = [
    "mercedes", "bmw", "audi", "porsche", "ferrari", "lamborghini",
    "bentley", "rolls-royce", "aston martin", "toyota", "honda", "ford",
    "tesla", "lexus", "range rover", "land rover", "jaguar", "maserati",
    "mclaren", "bugatti", "chevrolet", "nissan", "hyundai", "kia",
]

COMMON_COLORS = [
    "black", "white", "silver", "blue", "red", "grey", "gray", "green",
    "yellow", "orange", "brown", "gold",
]

BODY_STYLE_HINTS = {
    "suv": "suv", "suvs": "suv", "sedan": "sedan", "coupe": "coupe",
    "convertible": "convertible", "hatchback": "hatchback",
    "truck": "truck", "van": "van", "minivan": "van",
}


def parse_natural_query(text: str) -> dict:
    """Parse a free-text search like a sales consultant would."""
    text_lower = text.lower()
    result = {}

    # Price ceiling: "under $170,000" / "under 170000" / "below 75k"
    price_match = re.search(r"(?:under|below|less than)\s*\$?([\d,]+)\s*(k)?", text_lower)
    if price_match:
        raw = price_match.group(1).replace(",", "")
        value = int(raw)
        if price_match.group(2):
            value *= 1000
        result["price_max"] = value

    price_min_match = re.search(r"(?:over|above|more than)\s*\$?([\d,]+)\s*(k)?", text_lower)
    if price_min_match:
        raw = price_min_match.group(1).replace(",", "")
        value = int(raw)
        if price_min_match.group(2):
            value *= 1000
        result["price_min"] = value

    # Year: "2022 Toyota Camry"
    year_match = re.search(r"\b(19|20)\d{2}\b", text_lower)
    if year_match:
        result["year"] = int(year_match.group(0))

    # Make
    for make in COMMON_MAKES:
        if make in text_lower:
            result["make"] = make.title()
            break

    # Color
    for color in COMMON_COLORS:
        if re.search(rf"\b{color}\b", text_lower):
            result["exterior_color"] = color
            break

    # Body style
    for hint, style in BODY_STYLE_HINTS.items():
        if hint in text_lower:
            result["body_style"] = style
            break

    # Electric / hybrid
    if "electric" in text_lower or "ev" in text_lower.split():
        result["fuel_type"] = "electric"
    elif "hybrid" in text_lower:
        result["fuel_type"] = "hybrid"

    # AWD / 4WD
    if "awd" in text_lower or "all-wheel" in text_lower or "all wheel" in text_lower:
        result["drivetrain"] = "awd"
    elif "4wd" in text_lower or "four-wheel" in text_lower:
        result["drivetrain"] = "4wd"

    # Model: naive heuristic — word right after the make, if the make was found
    if "make" in result:
        pattern = rf"{result['make'].lower()}\s+([a-z0-9\-]+)"
        model_match = re.search(pattern, text_lower)
        if model_match:
            result["model"] = model_match.group(1).upper() if len(model_match.group(1)) <= 4 else model_match.group(1).title()

    return result
