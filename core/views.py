# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Task, User  # Replace `taskmanager` with your app name
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Check if the user is Admin or SuperAdmin
def is_admin(user):
    return user.role in ['ADMIN', 'SUPERADMIN']

@login_required(login_url="/login/")
def admin_dashboard_view(request):
    view_type = request.GET.get("view", "users")
    context = {"view_type": view_type}
    context["users"] = User.objects.all()
    context["tasks"] = Task.objects.all()
    return render(request, "admin_dashboard.html", context)

# @login_required
# @user_passes_test(is_admin)
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {'task': task}
    return render(request, 'task_detail.html', context)

def dashboard(request):
        return render(request, 'user_dashboard.html', {'user': "user"})

def user_login(request):
    if request.method == "POST":
        print("POST request received for login")
        form = AuthenticationForm(request, data=request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            print(user.role)
            login(request, user)
            if user.role == 'SUPERADMIN':
                messages.success(request, "Users cannot log in directly. Please contact your Admin.")
                return redirect("admin_dashboard")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = ""

    return render(request, "user_login.html", {"form": form})
