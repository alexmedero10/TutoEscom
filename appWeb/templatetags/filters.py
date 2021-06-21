from django import template

register = template.Library()

@register.filter
def getComments(obj, post_id):
    return obj.comments(post_id)
