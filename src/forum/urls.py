from django.urls import path

from forum.views import (Conversations, CreateComment, CreatePost, DetailPost,
                         GeneratorObjects)

app_name = "forum"
urlpatterns = [
    path("", Conversations.as_view(), name="forum"),
    path("<int:pk>/", DetailPost.as_view(), name="detail"),
    path("create-comment/<int:pk>/", CreateComment.as_view(), name="create_comment"),
    path("create-post/", CreatePost.as_view(), name="create_post"),
    path("generate/", GeneratorObjects.as_view(), name="generate")
]
