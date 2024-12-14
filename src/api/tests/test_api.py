from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_202_ACCEPTED,
                                   HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient

from problems.models import Category, Tasks
from problems.utils.samples import sample_task, sample_tests


class TestApi(TestCase):
    def setUp(self):
        tests_dir = f"{Path(__file__).resolve().parent.parent.parent}/problems/tasks/tests_for_tasks"
        self.client = APIClient()

        self.test = sample_tests(tests_dir)
        self.category = Category.objects.create(category="db")
        self.problem = sample_task("test", self.test, category=self.category)

        self.user = get_user_model()(username="testuser", email="testuser@example.com")
        self.user.set_password("testuser123")
        self.user.save()
        self.superuser = get_user_model()(
            username="testsuper", email="testsuperuser@example.com"
        )
        self.superuser.set_password("testuser123")
        self.superuser.is_staff = True
        self.superuser.is_superuser = True
        self.superuser.save()

    def test_api_get_problem(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse(
                "api:problems_detail_api",
                kwargs={
                    "pk": self.problem.pk,
                },
            )
        )

        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "test",
                "description": "test task description",
                "constraints": "test constraints",
                "category": 1,
                "difficulty": "Medium",
            },
        )

    def test_api_update_problem(self):
        self.client.force_authenticate(user=self.superuser)

        obj = self.client.patch(
            reverse("api:problems_update_api", kwargs={"pk": 1}), data={"name": "test2"}
        )

        self.assertEqual(obj.status_code, HTTP_200_OK)

        self.assertEqual(Tasks.objects.get(id=1).name, "test2")

    def test_api_get_problem_without_auth(self):
        response = self.client.get(
            reverse(
                "api:problems_detail_api",
                kwargs={
                    "pk": self.problem.pk,
                },
            )
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_withoutpermission_delete(self):
        self.client.force_authenticate(user=self.user)

        obj = self.client.post(reverse("api:problems_delete_api", kwargs={"pk": 1}))

        self.assertEqual(obj.status_code, HTTP_403_FORBIDDEN)

    def test_withpermission_delete(self):
        self.client.force_authenticate(user=self.superuser)

        obj = self.client.delete(reverse("api:problems_delete_api", kwargs={"pk": 1}))

        self.assertEqual(obj.status_code, HTTP_204_NO_CONTENT)
