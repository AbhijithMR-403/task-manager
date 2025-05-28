# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Task, User  # Replace `taskmanager` with your app name

# Check if the user is Admin or SuperAdmin
def is_admin(user):
    return user.role in ['ADMIN', 'SUPERADMIN']

# @login_required
# @user_passes_test(is_admin)
def admin_dashboard_view(request):
    users = User.objects.filter(role='USER')
    context = {'users': users}
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {'task': task}
    return render(request, 'task_detail.html', context)

def dashboard(request):
    # user = request.user

    # if user.role == 'SUPERADMIN':
    #     return redirect('admin_dashboard')
    # elif user.role == 'ADMIN':
    #     return redirect('admin_dashboard')
    # else:
        return render(request, 'user_dashboard.html', {'user': "user"})
