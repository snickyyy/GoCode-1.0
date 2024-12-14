from django.template import Library

register = Library()


@register.filter
def get_status_by_user(obj, args):
    return obj.get_task_status(args)
