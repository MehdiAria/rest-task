from django.http import JsonResponse
from django.urls import path


def health(_: object) -> JsonResponse:
    return JsonResponse({"status": "ok"})


urlpatterns = [path("health/", health, name="health")]
