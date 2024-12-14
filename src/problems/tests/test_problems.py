from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from problems.models import Category, Language, Solutions, Tasks
from problems.utils.samples import sample_solution, sample_task, sample_tests


class TestProblems(TestCase):
    def setUp(self):
        tests_dir = f"{Path(__file__).resolve().parent.parent}/tasks/tests_for_tasks"
        self.test_tests = sample_tests(tests_dir)

        self.category = Category.objects.create(category="Math")

        self.test_problem = sample_task("Two sums", self.test_tests, self.category)

    def test_count_problem(self):
        self.assertEqual(Tasks.objects.count(), 1)

    def test_max_limit_name_task(self):
        with self.assertRaises(ValidationError):
            sample_task("N" * 500, self.test_tests, self.category)

    def test_max_limit_description_task(self):
        with self.assertRaises(ValidationError):
            sample_task("U" * 5000, self.test_tests, self.category)


class TestSolutions(TestCase):
    def setUp(self):
        tests_dir = f"{Path(__file__).resolve().parent.parent}/tasks/tests_for_tasks"
        self.test_tests = sample_tests(tests_dir)

        self.category = Category.objects.create(category="Math")

        self.task = sample_task("Two sums", self.test_tests, self.category)

        self.client = Client()

        self.user = get_user_model()(username="Oleg")
        self.user.set_password("12345678")
        self.user.save()

        self.language = Language.objects.create(language="Python")

        self.solution = sample_solution(self.user, self.task, self.language)

    def test_solution(self):
        self.assertEqual(Solutions.objects.count(), 1)
