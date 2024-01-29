from django.urls import path

from . import views
from .views import MakeContract

app_name = "hospital_contract"
urlpatterns = [
    path("make-contract/", MakeContract.as_view(), name="make-contract")
]


