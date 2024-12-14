from django.contrib import admin

from problems.models import Category, Language, Solutions, Tasks, Tests

# Register your models here.


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin): ...


@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin): ...


@admin.register(Solutions)
class SolutionAdmin(admin.ModelAdmin): ...


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin): ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): ...
