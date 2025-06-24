from django import template
from django.utils.safestring import mark_safe

from acrofestival.content.snippets import get_snippet

register = template.Library()


@register.simple_tag
def content_snippet(key: str, default: str = "") -> str:
    """
    Template tag to retrieve a content snippet.
    Usage: {% content_snippet 'email_whatsapp' %}
    """
    content = get_snippet(key, default)
    return mark_safe(content)