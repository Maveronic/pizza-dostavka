from django.urls import path
from authentication.views import UserCreateView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
]
