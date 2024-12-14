from time import sleep

from celery import shared_task

from forum.models import Comments, Conversation


@shared_task
def mine_bitcoin():
    sleep(15)


@shared_task
def generate_posts_and_comments(count_posts, count_comments):
    Conversation.generate_conversations(count_posts)
    Comments.generate_comments(count_comments)
    sleep(10)
