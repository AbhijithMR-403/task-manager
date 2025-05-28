from django.urls import path, include
from .views import admin_dashboard_view, task_detail_view, dashboard, user_login  # Add your template views here

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),                          # Main dashboard (template view)
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('task/<int:task_id>/', task_detail_view, name='task_detail'),

    path("login/", user_login, name="user_login"),

    path('api/', include('core.api.urls')),                         # DRF API routes
]
