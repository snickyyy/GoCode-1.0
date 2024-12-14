from django.template import Library

from forum.models import Comments, Conversation

register = Library()


@register.filter
def get_count_comments(obj):
    return Comments.objects.filter(conversation=obj).count()


@register.simple_tag
def get_all_posts_by_user(pk):
    return Conversation.objects.filter(author_id=pk).count()


@register.simple_tag
def get_all_comments_by_user(pk):
    return Comments.objects.filter(author_id=pk).count()


@register.simple_tag
def get_newest_comment_by_post(obj):
    last_comment = obj.comments.order_by('-created_at').first()
    return last_comment
