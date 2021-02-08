from django.urls import path, re_path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('profile/', authapp.profile, name='profile'),
    path('register/', authapp.register, name='register'),
    # re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
    path('verify/<email>/<activation_key>', authapp.verify, name='verify'),
]
