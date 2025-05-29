# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from core.models import Task, User  # Replace `taskmanager` with your app name
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def admin_dashboard_view(request):
    if request.user.role not in ['SUPERADMIN', 'ADMIN']:
        messages.error(request, "You do not have permission to access that page.")
        return redirect('home')
    view_type = request.GET.get("view", "tasks")
    context = {"view_type": view_type}
    if request.user.role == "SUPERADMIN":
        context["users"] = User.objects.all()
        context["tasks"] = Task.objects.all()
    else:
        assigned_users = User.objects.filter(assigned_admin=request.user.id)
        context["users"] = assigned_users
        context["tasks"] = Task.objects.filter(assigned_to__in=assigned_users)

    return render(request, "admin_dashboard.html", context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {'task': task}
    context["users"] = User.objects.filter(role='USER')

    return render(request, 'task_detail.html', context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_page(request):
    user = request.user
    context = {"tasks": Task.objects.filter(assigned_to=user)}
    return render(request, 'user_dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'SUPERADMIN':
                messages.success(request, "Successfully Logged in as 'SuperAdmin'.")
                return redirect("admin_dashboard")
            elif user.role == 'ADMIN':
                messages.success(request, "Successfully Logged in as 'Admin'.")
                return redirect("admin_dashboard")
            else:
                messages.success(request, "Successfully Logged in as 'User'.")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = ""
    return render(request, "user_login.html", {"form": form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_user_edit_form(request, user_id):
    user = get_object_or_404(User, id=user_id)
    admins = User.objects.filter(Q(role='ADMIN') | Q(role='SUPERADMIN'))
    return render(request, 'edit_user.html', {
        'user': user,
        'admins': admins
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('user_login')

@login_required
def delete_user(request, user_id):
    url = reverse('admin_dashboard') + "?view=users"
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete users.")
        return redirect(url)
    if str(request.user.id) == str(user_id):
        messages.error(request, "You cannot delete your own account.")
        return redirect(url)

    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        messages.error(request, "You cannot delete a superuser.")
        return redirect(url)

    user.delete()
    messages.success(request, f"User '{user.username}' deleted successfully.")
    return redirect(url)

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    url = reverse('admin_dashboard') + "?view=tasks"

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect(url)

    messages.error(request, "Invalid request.")
    return redirect(url)
