from django.urls import path

from problems.views import SolvedTask, Task, TaskList

app_name = "problems"
urlpatterns = [
    path("list/", TaskList.as_view(), name="list"),
    path("<int:pk>/", Task.as_view(), name="selected_task"),
    path("<int:pk>/sumbit/", SolvedTask.as_view(), name="solved_task"),
]
