from django.urls import path, include
from .views import admin_dashboard_view, delete_user, get_user_edit_form, logout_view, task_detail_view, home_page, user_login  # Add your template views here

urlpatterns = [
    path('', home_page, name='home'),
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('task/<int:task_id>/', task_detail_view, name='task_detail'),

    path("login/", user_login, name="user_login"),
    path('logout/', logout_view, name='logout'),
    path('admin/get_user_update_form/<int:user_id>/', get_user_edit_form, name='get_user_edit_form'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),

    path('api/', include('core.api.urls')),
]
