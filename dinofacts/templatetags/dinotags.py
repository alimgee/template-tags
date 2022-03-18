from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape, mark_safe, escape


register = template.Library()

@register.filter
def first_letters(iterable):
    ''' basic tag that returns the first letter in an iterable'''
    result = ""
    for item in iterable:
        result += item[0]

    return result


@register.filter(name="nth_letters", is_safe=True)
def other_letters(iterable, num):
    ''' tag that returns the letter at num value for each iteration'''
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
    ''' string tag example - returns a string to the page'''
    if autoescape:
        value = conditional_escape(value)

    result = (
        f"<i>{value}</i> has <b>{value.count(letter)}</b> "
        f"instance(s) of the letter <b>{letter}</b>"
    )

    return mark_safe(result)


@register.filter(expects_localtime=True)
def bold_time(when):
    ''' tag that returns local time'''
    return mark_safe(f"<b>{when}</b>")


@register.simple_tag
def mute(*args):
    '''simple custom tag without filter'''
    return ""


@register.simple_tag
def make_ul(iterable):
    ''' simple tage that auto escapes html list'''
    content = ["<ul>"]
    for item in iterable:
        content.append(f"<li>{escape(item)}</li>")

    content.append("</ul>")
    content = "".join(content)
    return mark_safe(content)


@register.simple_tag(takes_context=True)
def dino_list(context, title):
    output = [f"<h2>{title}</h2><ul>"]
    for dino in context["dinosaurs"]:
        output.append(f"<li>{escape(dino)}</li>")

    output.append("</ul>")
    output = "".join(output)

    context["weight"] = "20 tons"
    return mark_safe(output)


@register.inclusion_tag("sublist.html")
def include_list(iterator):
    return {"iterator": iterator}


# Advanced tags 

import mistune

@register.tag(name="markdown")
def do_markdown(parser, token):
    nodelist = parser.parse(("endmarkdown",))
    parser.delete_first_token()
    return MarkdownNode(nodelist)

class MarkdownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        result = mistune.markdown(str(content))
        return result


@register.tag()
def shownodes(parser, token):
    nodelist = parser.parse(("endshownodes",))
    parser.delete_first_token()
    return ShowNodesNode(token, nodelist)

class ShowNodesNode(template.Node):
    def __init__(self, token, nodelist):
        self.token = token
        self.nodelist = nodelist

    def render(self, context):
        result = [
            "<ul><li>Token info:</li><ul>",
        ]

        for part in self.token.split_contents():
            content = escape(str(part))
            result.append(f"<li>{content}</li>")

        result.append("</ul><li>Block contents:</li><ul>")
        for node in self.nodelist:
            content = escape(str(node))
            result.append(f"<li>{content}</li>")

        result.append("</ul>")
        return "".join(result)