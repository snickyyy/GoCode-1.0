import os
from random import choice, randint

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, SET_DEFAULT
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from faker import Faker

from common.models import BaseModel

# Create your models here.


class DIFFICULTLY_CHOICES(models.IntegerChoices):
    EASY = 0, "Easy"
    MEDIUM = 1, "Medium"
    HARD = 2, "Hard"


class TASK_STATUS_CHOICES(models.IntegerChoices):
    IN_DEVELOPMENT = 0, "In-Development"
    ACCEPTED = 1, "Accepted"


class Category(BaseModel):
    category = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.category}"

    @classmethod
    def generate_categories(cls):
        categories = []
        choices = ["Math", "db", "algorithms"]
        for i in choices:
            category = Category(category=f"{i}")
            categories.append(category)
        result = Category.objects.bulk_create(categories)
        return result


class Language(BaseModel):
    language = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.language}"

    @classmethod
    def generate_languages(cls):
        languages = []
        choices = ["Python", "Java", "JavaScript", "C#", "C++"]
        for i in choices:
            language = Language(language=f"{i}")
            languages.append(language)
        result = Language.objects.bulk_create(languages)
        return result


class Tasks(BaseModel):
    name = models.CharField(
        max_length=280,
        unique=True,
        help_text=_("Name must be unique and max length is 280 characters."),
    )
    difficulty = models.PositiveSmallIntegerField(
        choices=DIFFICULTLY_CHOICES.choices, default=DIFFICULTLY_CHOICES.MEDIUM
    )
    category = models.ForeignKey(Category, on_delete=CASCADE)
    description = models.TextField(max_length=2400)
    constraints = models.CharField(max_length=240)
    tests = models.ForeignKey("problems.Tests", on_delete=CASCADE)
    photo = models.ImageField(upload_to="tasks/images", null=True, blank=True)

    def __str__(self):
        return f"({self.pk}){self.name} {self.difficulty} {self.category} {self.created_at}"

    @classmethod
    def generate_tasks(cls, count):
        tasks = []
        faker = Faker()
        for i in range(count):
            task = Tasks(
                name=faker.sentence(nb_words=5),
                difficulty=randint(0, 2),
                category=choice(Category.objects.all()),
                description=faker.text(max_nb_chars=2400),
                constraints=faker.text(max_nb_chars=240),
                tests=choice(Tests.objects.all()),
                photo=faker.image_url(),
            )
            tasks.append(task)
        result = Tasks.objects.bulk_create(tasks)
        return result

    def get_task_status(self, user_id):
        try:
            solution = Solutions.objects.get(task=self, user_id=user_id)
            return solution.status
        except Solutions.DoesNotExist:
            return None

    def get_count_solutions(self):
        return Solutions.objects.filter(task=self).count()


class Tests(BaseModel):
    count_tests = models.IntegerField()
    tests = models.FileField(upload_to="data_tests/")

    def __str__(self):
        return f"({self.pk}){self.tests} {self.count_tests}"

    @classmethod
    def generate_tests(cls, count):
        tests = []
        faker = Faker()
        for i in range(count):
            test = Tests(
                count_tests=count,
                tests=f"problems/tasks/tests_for_tasks/{faker.file_path()}",
            )
            tests.append(test)
        result = Tests.objects.bulk_create(tests)
        return result


class Solutions(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=CASCADE, related_name="user")
    task = models.ForeignKey(Tasks, on_delete=CASCADE, related_name="solution")
    language = models.ForeignKey(
        Language,
        on_delete=CASCADE,
        related_name="solution_language",
    )
    solution = models.TextField(max_length=4200)
    status = models.PositiveSmallIntegerField(
        choices=TASK_STATUS_CHOICES.choices, default=TASK_STATUS_CHOICES.IN_DEVELOPMENT
    )
    time = models.PositiveIntegerField()
    memory = models.FloatField()
    test_passed = models.PositiveIntegerField()

    def __str__(self):
        return f"({self.pk}){self.user.username} {self.task.name} {self.language} status: {self.status} memory: {self.memory}mb time: {self.time}ms test_passed: {self.test_passed}"

    def get_date(self):
        return (timezone.now() - self.last_updated).days

    @classmethod
    def generate_solutions(cls, count):
        solutions = []
        faker = Faker()
        for i in range(count):
            user = choice(get_user_model().objects.all())
            task = choice(Tasks.objects.all())
            language = choice(Language.objects.all())
            solution = Solutions(
                user=user,
                task=task,
                language=language,
                solution=faker.text(max_nb_chars=4200),
                status=randint(0, 1),
                time=randint(1, 1000),
                memory=randint(1, 1000),
                test_passed=randint(0, 100),
            )
            solutions.append(solution)
        result = Solutions.objects.bulk_create(solutions)
        return result
