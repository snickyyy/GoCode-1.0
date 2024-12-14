from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (GoUserViewSet, ProblemCreateView, ProblemDeleteView,
                       ProblemDetailView, ProblemsListView, ProblemsUpdateView,
                       SolutionGetVew, SolutionListView)

router = routers.DefaultRouter()
router.register("users", GoUserViewSet)
app_name = "api"

# POST gamers/
# GET gamers/
# GET gamers/<id>/
# PUT gamers/<id>/
# PATCH gamers/<id>/
# DELETE gamers/<id>/

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

problems_urls = [
    path(
        "problems/retrieve/<int:pk>",
        ProblemDetailView.as_view(),
        name="problems_detail_api",
    ),
    path("problems/create/", ProblemCreateView.as_view(), name="problems_create_api"),
    path(
        "problems/update/<int:pk>",
        ProblemsUpdateView.as_view(),
        name="problems_update_api",
    ),
    path(
        "problems/delete/<int:pk>",
        ProblemDeleteView.as_view(),
        name="problems_delete_api",
    ),
    path("problems/list/", ProblemsListView.as_view(), name="problems_list"),
]

solution_urls = [
    path("solutions/get/<int:pk>", SolutionGetVew.as_view(), name="solution_get"),
    path("solutions/list/", SolutionListView.as_view(), name="solutions_list"),
]


urlpatterns = [
    path("", include(router.urls)),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("auth/", include("djoser.urls.jwt")),
]
urlpatterns += problems_urls
urlpatterns += solution_urls
