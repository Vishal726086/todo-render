from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# todo/views.py
from django.contrib.auth.views import LogoutView
from . views import CustomLogoutView
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path('', views.index, name='index'),
    path('task/add/', views.add_task, name='add_task'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),  # ✅ use custom view here
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', views.mark_complete, name='mark_complete'),
    path('toggle/<int:task_id>/', views.toggle_complete, name='toggle_complete'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

]
