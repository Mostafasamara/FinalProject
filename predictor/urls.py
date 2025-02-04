from django.urls import path
from .views import PredictStudentPerformance



urlpatterns = [
    path("predict/", PredictStudentPerformance.as_view(), name="predict"),

]
