from django.urls import path
from . import views 

app_name = "houses"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<int:pk>", views.HouseDetail.as_view(), name="detail"),
    path("create/", views.CreateHouseView.as_view(), name="create"),
    path("<int:pk>/edit/", views.EditHouseView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.HousePhotosView.as_view(), name="photos"),
    path(
        "<int:house_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="add-photos"),
    path("search/", views.SearchView.as_view(), name="search"),
]