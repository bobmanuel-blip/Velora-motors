from django.urls import path

from . import views

app_name = "chatapp"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("start/<int:vehicle_pk>/", views.start_conversation, name="start_conversation"),
    path("<int:pk>/", views.conversation_detail, name="conversation_detail"),
    path("<int:pk>/poll/", views.poll_messages, name="poll_messages"),
]
