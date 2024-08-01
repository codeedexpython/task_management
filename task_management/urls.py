"""
URL configuration for task_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('login',views.user_login),
    path('forgot_password',views.request_otp),
    path('verify_otps',views.verify_otps),
    path('logout', views.logout, name='logout'),
    path('registration',views.registration),
    path('otp_verify',views.otp_verify),
    path('profile',views.profile),
    path('edit_profile',views.edit_profile),
    path('personal_task',views.personal_task),
    path('add_personal_task',views.create_personal_task),
    path('view_personal_task',views.personal_task_list),
    path('update_personal_task/<int:personal_task_id>',views.update_personal_task),
    path('remove/<int:personal_task_id>',views.remove_personal_task),
    path('assigned_task',views.assigned_task_list),
    path('admin_assigned_task',views.view_assigned_tasks),
    path('team_assigned_task',views.team_management),
    path('project',views.project),
    path('edit_task/<int:task_id>',views.edit_task_status),
    path('edit_team/<int:task_id>/',views.edit_task),
    path('edit_project/<int:project_id>/',views.edit_project),
    path('report',views.report)
]
