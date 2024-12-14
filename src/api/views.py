from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsSuperUser
from api.serializers import (GoUserSerializer, ProblemGetSerializer,
                             ProblemSerializerCreate, ProblemSerializerDelete,
                             ProblemSerializerList, ProblemSerializerUpdate,
                             SolutionGetSerializer, SolutionListSerializer)
from problems.models import Solutions, Tasks

# Create your views here.


class GoUserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = GoUserSerializer


class ProblemDetailView(RetrieveAPIView):
    serializer_class = ProblemGetSerializer
    queryset = Tasks.objects.all()

    def get_object(self):
        return Tasks.objects.get(pk=self.kwargs.get("pk"))


class ProblemsListView(ListAPIView):
    queryset = Tasks.objects.all()
    serializer_class = ProblemSerializerList


class ProblemCreateView(CreateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Tasks.objects.all()
    serializer_class = ProblemSerializerCreate


class ProblemsUpdateView(UpdateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Tasks.objects.all()
    serializer_class = ProblemSerializerUpdate

    def get_serializer(self, *args, **kwargs):
        kwargs["pk"] = self.kwargs.get("pk")
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        return super().get_object()


class ProblemDeleteView(DestroyAPIView):
    permission_classes = [IsSuperUser]
    queryset = Tasks.objects.all()
    serializer_class = ProblemSerializerDelete


class SolutionGetVew(RetrieveAPIView):
    queryset = Solutions.objects.all()
    serializer_class = SolutionGetSerializer


class SolutionListView(ListAPIView):
    queryset = Solutions.objects.all()
    serializer_class = SolutionListSerializer

    def get_queryset(self):
        problem_pk = self.request.query_params.get("pk")
        if problem_pk:
            return Solutions.objects.filter(id=problem_pk)
        return super().get_queryset()
