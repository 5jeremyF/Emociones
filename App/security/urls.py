from django.urls import path

from App.security.views.auth import LogLoginView, RegisterView, cerrarSesion
from App.security.views.user import LogSignUpView

app_name = "security"
urlpatterns = []

urlpatterns += [
    path('login/', LogLoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('logout/', cerrarSesion, name='logout'),
]
