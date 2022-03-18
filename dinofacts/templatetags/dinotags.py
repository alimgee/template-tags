from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape, mark_safe


register = template.Library()

@register.filter
def first_letters(iterable):
    result = ""
    for item in iterable:
        result += item[0]

    return result


@register.filter(name="nth_letters", is_safe=True)
def other_letters(iterable, num):
    result = ""
    for item in iterable:
        if len(item) <= num or not item[num - 1].isalpha():
            result += " "
        else:
            result += item[num - 1]

    return result


@register.filter(needs_autoescape=True)
@stringfilter
def letter_count(value, letter, autoescape=True):
    if autoescape:
        value = conditional_escape(value)

    result = (
        f"<i>{value}</i> has <b>{value.count(letter)}</b> "
        f"instance(s) of the letter <b>{letter}</b>"
    )

    return mark_safe(result)