import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from problems.forms import EditorForm
from problems.models import Category, Language, Solutions, Tasks
from problems.redis.utils import (add_in_queue, check_user_in_queue,
                                  wait_and_get_result)
from problems.utils.validators import validate_code

# Create your views here.


class TaskList(ListView):
    paginate_by = 25
    template_name = "task_list.html"
    queryset = Tasks.objects.all()
    context_object_name = "tasks"

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        search_task = request.GET.get("search-task", False)
        category = request.GET.get("category", False)
        if search_task:
            return render(
                request,
                "task_list.html",
                context={"tasks": Tasks.objects.filter(name__icontains=search_task)},
            )
        elif category:
            try:
                get_category = Category.objects.get(category=category)
            except Category.DoesNotExist:
                return HttpResponse("Category does not exist.")
            return render(
                request,
                "task_list.html",
                context={"tasks": Tasks.objects.filter(category=get_category)},
            )
        return super().get(request, *args, **kwargs)


class Task(TemplateView):
    template_name = "selected_task.html"
    form_class = EditorForm
    task = None
    task_tests = None
    model = Solutions
    start = """def {name}(**kwargs):\n\tpass"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.task = Tasks.objects.get(pk=kwargs.get("pk", None))
        if self.task is None:
            return HttpResponse("No such task")
        context["task"] = self.task
        context["form"] = self.form_class(self.request.POST or None, initial={"text": self.format_start_code()})
        return context

    def get_start_code(self):
        try:
            code = Solutions.objects.get(task=self.task, user_id=self.request.user.id).solution
            return True, code
        except Solutions.DoesNotExist:
            return False, self.start

    def format_start_code(self):
        start = self.get_start_code()
        if start[0]:
            return start[1]

        name = self.task.name.replace(" ", "_").lower()
        return start[1].format(name=name)


class SolvedTask(TemplateView):
    template_name = "solved_task.html"
    form_class = EditorForm
    queue_data_name = "data"
    queue_pk_name = "pks"
    queue_result_name = "results"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # task = Tasks.objects.get(id=kwargs.get("pk"))
        if form.is_valid():
            code = form.cleaned_data["text"]
            is_valid_code = validate_code(code)
            if not is_valid_code[0]:
                return HttpResponse(f"Name '{is_valid_code[1]}' is not available, use another one")
            if check_user_in_queue(self.request.user.pk):
                return HttpResponse("you can't s sumbit 2 tasks at once")
            test = task.tests.tests.name
            data = json.dumps({"pk": self.request.user.pk, "code": code, "test_name": test.split("/")[-1]})

            add_in_queue(data, self.request.user.pk)

            result = wait_and_get_result(self.request.user.pk)

            update_solution = Solutions.objects.filter(
                user_id=self.request.user.pk,
                task=task
            ).update(
                status=result.get("status"),
                test_passed=result.get("successful_tests"),
                solution=code,
            )
            if not update_solution:
                solution = Solutions(
                    task=task,
                    user=request.user,
                    language=Language.objects.get(language="Python"),
                    solution=code,
                    status=result.get("status"),
                    time=16,
                    memory=4,
                    test_passed=result.get("successful_tests"),
                )
                solution.save()
            return render(
                request,
                self.template_name,
                context={"result": result},
            )
