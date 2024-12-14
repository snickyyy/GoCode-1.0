from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework.fields import CharField, FileField, IntegerField
from rest_framework.serializers import ModelSerializer

from problems.models import Solutions, Tasks, Tests


class GoUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "description", "is_staff"]


class ProblemGetSerializer(ModelSerializer):
    difficulty = CharField(source="get_difficulty_display")
    # tests = FileField(source="tests.tests")
    # count_tests = IntegerField(source="tests.count_tests")

    class Meta:
        model = Tasks
        fields = ["id", "name", "description", "constraints", "category", "difficulty"]


class ProblemSerializerCreate(ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            "name",
            "description",
            "difficulty",
            "constraints",
            "tests",
            "category",
            "photo",
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance


class ProblemSerializerUpdate(ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            "name",
            "description",
            "difficulty",
            "constraints",
            "tests",
            "category",
            "photo",
        ]

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Получаем pk, если он передан
        super().__init__(*args, **kwargs)

    def update(self, instance: Tasks, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProblemSerializerList(ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"


class ProblemSerializerDelete(ModelSerializer):
    class Meta:
        model = Tasks


class SolutionGetSerializer(ModelSerializer):
    class Meta:
        model = Solutions
        fields = "__all__"


class SolutionListSerializer(ModelSerializer):
    class Meta:
        model = Solutions
        fields = "__all__"
