from django.urls import path, include
from .views import admin_dashboard_view, task_detail_view, dashboard  # Add your template views here

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),                          # Main dashboard (template view)
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('task/<int:task_id>/', task_detail_view, name='task_detail'),
    
    path('api/', include('core.api.urls')),                         # DRF API routes
]
