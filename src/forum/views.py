from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView

from forum.models import Comments, Conversation
from forum.tasks import generate_posts_and_comments


class Conversations(ListView):
    paginate_by = 25
    template_name = "conversations.html"
    queryset = Conversation.objects.all()
    context_object_name = "conversations"

    def get(self, request, *args, **kwargs):
        search_conversation = request.GET.get("search", False)
        if search_conversation:
            self.queryset = self.queryset.filter(title__icontains=search_conversation)
        elif request.GET.get("sorted", False):
            sort_prefix = {
                "all": self.queryset,
                "oldest": self.queryset.order_by('created_at'),
                "newest": self.queryset.order_by('-created_at'),
                "m_comments": self.queryset.annotate(count_comments=Count("comments")).order_by("-count_comments"),
                "l_comments": self.queryset.annotate(count_comments=Count("comments")).order_by("count_comments"),
            }
            self.queryset = sort_prefix.get(request.GET.get("sorted", False))
        return super().get(request, *args, **kwargs)


class DetailPost(TemplateView):
    template_name = "detail_post.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        conversation = Conversation.objects.get(pk=pk)
        comments = Comments.objects.filter(conversation=conversation).order_by("created_at")
        return super().get_context_data(conversation=conversation, comments=comments, **kwargs)


class CreateComment(CreateView):
    model = Comments

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return HttpResponse("Conversation not found")
        Comments.objects.create(author=self.request.user, conversation=conversation, content=request.POST.get("reply"))
        return redirect(reverse_lazy("forum:detail", kwargs={"pk": pk}))


class CreatePost(CreateView):
    model = Conversation
    template_name = "create_post.html"
    fields = ["title", "content", "image"]

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        content = request.POST.get("content")
        conversation = Conversation.objects.create(title=title, content=content, author=self.request.user, image=request.FILES.get("image"))
        return redirect(reverse_lazy("forum:detail", kwargs={"pk": conversation.pk}))


class GeneratorObjects(View):
    """Before using it, it is better to familiarize yourself with how the generation method works in models"""
    def get(self, request, *args, **kwargs):
        generate_posts_and_comments.delay(request.GET.get("posts", 1), request.GET.get("comments", 5))
        return HttpResponse("Add task")
