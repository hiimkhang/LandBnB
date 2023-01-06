from django.urls import path
from house import views as house_views

app_name = "core"
urlpatterns = [
    path("", house_views.HomeView.as_view(), name="home"),
    # path("", house_views.all_houses)
]