# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Task, User  # Replace `taskmanager` with your app name
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control

# Check if the user is Admin or SuperAdmin
def is_admin(user):
    return user.role in ['ADMIN', 'SUPERADMIN']
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def admin_dashboard_view(request):
    view_type = request.GET.get("view", "users")
    context = {"view_type": view_type}
    context["users"] = User.objects.all()
    context["tasks"] = Task.objects.all()
    return render(request, "admin_dashboard.html", context)

# @login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {'task': task}
    context["users"] = User.objects.filter(role='USER')

    return render(request, 'task_detail.html', context)

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
        print("POST request received for login")
        form = AuthenticationForm(request, data=request.POST)
        print(request.POST)
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