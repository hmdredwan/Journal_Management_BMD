from django import template

register = template.Library()

@register.filter
def thumbnail_url(paper):
    try:
        if paper.thumbnail and paper.thumbnail.name:
            return paper.thumbnail.url
    except ValueError:
        pass
    return None
