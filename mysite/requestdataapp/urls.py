from django.urls import path

from .views import process_get_views, user_form, handle_file_upload
from .middlewares import set_useragent_on_request_middleware

app_name = "requestdataapp"

urlpatterns = [
    path("get/", process_get_views, name="get-view"),
    path("bio/", user_form, name="user-form"),
    path("upload/", handle_file_upload, name="file-upload"),
]