from problems.models import TASK_STATUS_CHOICES, Solutions, Tasks, Tests


def sample_tests(path, **kwargs):
    default = {
        "count_tests": 10,
        "tests": path,
    }
    default.update(kwargs)
    return Tests.objects.create(**default)


def sample_task(title: str, tests, category, **kwargs):
    default = {
        "name": title,
        "description": "test task description",
        "constraints": "test constraints",
        "tests": tests,
        "category": category,
    }
    default.update(kwargs)
    return Tasks.objects.create(**default)


def sample_solution(user, task, language, **kwargs):
    default = {
        "user": user,
        "task": task,
        "language": language,
        "solution": "print('Hello, World!')",
        "status": TASK_STATUS_CHOICES.ACCEPTED,
        "time": 16,
        "memory": 20,
        "test_passed": 108,
    }
    default.update(kwargs)
    return Solutions.objects.create(**default)
