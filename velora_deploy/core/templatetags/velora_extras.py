from django import template

register = template.Library()


@register.filter
def split_comma(value):
    """Splits 'Leather Seats, Sunroof, Heated Steering' into a clean list."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]
