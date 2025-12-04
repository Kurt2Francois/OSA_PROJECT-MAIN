from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import UserProfile, Department
from .serializers import UserSerializer, DepartmentSerializer
from partnership.models import Department
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login




def ensure_default_department():
    if not Department.objects.exists():
        Department.objects.create(
            business_name="Default Business",
            department_name="Default Department",
            contact_person="Admin",
            contact_number="0000-0000",
            email="admin@example.com",
            partnership_status="OK"
        )

@login_required
def department_edit_view(request, dept_id):
    """
    Allows editing a department:
    - Owners can edit only their own department.
    - Admins and superusers can edit any department.
    """
    user_profile = getattr(request.user, 'profile', None)

    # Determine access
    if request.user.is_superuser or (user_profile and user_profile.user_type in ['admin']):
        # Admin/superuser can edit any department
        department = get_object_or_404(Department, id=dept_id)
    else:
        # Owners can only edit their own department
        department = get_object_or_404(Department, id=dept_id, owner=request.user)

    if request.method == 'POST':
        # Update text fields
        department.business_name = request.POST.get('business_name')
        department.department_name = request.POST.get('department_name')
        department.contact_person = request.POST.get('contact_person')
        department.contact_number = request.POST.get('contact_number')
        department.email = request.POST.get('email')
        department.partnership_status = request.POST.get('partnership_status')
        department.remarks_status = request.POST.get('remarks_status')

        # Update dates
        established_date = request.POST.get('established_date')
        expiration_date = request.POST.get('expiration_date')
        if established_date:
            department.established_date = established_date
        if expiration_date:
            department.expiration_date = expiration_date

        # Update logo if uploaded
        if 'logo_path' in request.FILES:
            department.logo_path = request.FILES['logo_path']

        department.save()
        messages.success(request, 'Department updated successfully!')

        # Redirect admins to admin panel, owners to department detail
        if request.user.is_superuser or (user_profile and user_profile.user_type in ['admin']):
            return redirect('admin_panel')
        else:
            return redirect('department_detail', dept_id=department.id)

    # Render the edit form
    return render(request, 'partnership/department_edit.html', {'department': department})

# -----------------------------
# Signup View
# -----------------------------
def signup_view(request):
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        department_name = request.POST.get('department_name')
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm_email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if email != confirm_email:
            messages.error(request, 'Emails do not match')
            return render(request, 'partnership/signup.html')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'partnership/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'partnership/signup.html')

        # Create User
        username = email.split('@')[0] + str(User.objects.count() + 1)
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            business_name=business_name,
            department_name=department_name,
            contact_person=contact_person,
            contact_number=contact_number,
            user_type='department'
        )

        # Create Department
        department = Department.objects.create(
            owner=user,
            business_name=business_name,
            department_name=department_name,
            contact_person=contact_person,
            contact_number=contact_number,
            email=email
        )

        # Auto-login user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('department_detail', dept_id=department.id)

    return render(request, 'partnership/signup.html')


# -----------------------------
# Login View
# -----------------------------
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User, Department

def login_view(request):
    # If user already logged in
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_panel')  # Superuser → admin panel
        else:
            # Normal users → first department or dashboard
            department = Department.objects.filter(owner=request.user).first()
            if department:
                return redirect('department_detail', dept_id=department.id)
            return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                
                # Superuser → admin panel
                if user.is_superuser:
                    return redirect('admin_panel')
                
                # Normal users → first department or dashboard
                department = Department.objects.filter(owner=user).first()
                if department:
                    return redirect('department_detail', dept_id=department.id)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'User not found')

    return render(request, 'partnership/login.html')



# -----------------------------
# Logout View
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------------
# Department Detail View
# -----------------------------
@login_required
def department_detail_view(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)

    # Restrict access: only superuser, admin, owner, or department owner
    user_profile = getattr(request.user, 'profile', None)
    if not (request.user.is_superuser or
            (user_profile and user_profile.user_type in ['admin', 'owner']) or
            department.owner == request.user):
        messages.error(request, "You do not have permission to view this department.")
        return redirect('dashboard')

    return render(request, 'partnership/department_detail.html', {'department': department})


# -----------------------------
# Placeholder Views for URLs
# -----------------------------
@login_required
def dashboard_view(request):
    # Ensure at least one default department exists
    if not Department.objects.exists():
        Department.objects.create(
            business_name="Default Business",
            department_name="Default Department",
            contact_person="Admin",
            contact_number="0000-0000",
            email="admin@example.com",
            partnership_status="OK"
        )

    # If the user is an owner/admin, show all departments, otherwise only their own
    user_profile = getattr(request.user, 'profile', None)
    
    if request.user.is_superuser or (user_profile and user_profile.user_type in ['owner', 'admin']):
        departments = Department.objects.all()
    else:
        departments = Department.objects.filter(owner=request.user)
    
    return render(request, 'partnership/dashboard.html', {
        'departments': departments
    })


@login_required
def owner_panel_view(request):
    # Ensure we get the UserProfile for the logged-in user
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None

    # Only show departments owned by the current user
    departments = Department.objects.filter(owner=request.user)

    context = {
        'user': profile,  # For user info in the template
        'user_email': request.user.email,
        'departments': departments
    }

    return render(request, 'partnership/owner_panel.html', context)

# Only allow admin users
def is_admin(user):
    return user.is_authenticated and user.profile.user_type == 'admin'

@login_required
def admin_panel_view(request):
    user_profile = getattr(request.user, 'profile', None)
    if not request.user.is_superuser and not (user_profile and user_profile.user_type in ['owner', 'admin']):
        messages.error(request, "You don't have permission to access Admin Panel.")
        return redirect('dashboard')

    # Handle POST requests for updating remarks
    if request.method == 'POST':
        dept_id = request.POST.get('department_id')
        remarks_status = request.POST.get('remarks_status')
        if dept_id and remarks_status is not None:
            department = get_object_or_404(Department, id=dept_id)
            department.remarks_status = remarks_status
            department.save()
            messages.success(request, f"Remarks for '{department.department_name}' updated successfully!")
        return redirect('admin_panel')  # redirect to avoid resubmission

    # Compute stats
    stats = {
        'total_departments': Department.objects.count(),
        'active_partnerships': Department.objects.filter(partnership_status='active').count(),
        'pending_partnerships': Department.objects.filter(partnership_status='pending').count(),
        'total_users': User.objects.count(),
    }

    departments = Department.objects.all()
    return render(request, 'partnership/admin_panel.html', {
        'stats': stats,
        'departments': departments,
        'user_email': request.user.email,  # optional, if you show email in template
    })


@login_required
def department_delete_view(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)

    user_profile = getattr(request.user, 'profile', None)
    if department.owner != request.user and not request.user.is_superuser and not (user_profile and user_profile.user_type in ['owner', 'admin']):
        messages.error(request, "You don't have permission to delete this department.")
        return redirect('dashboard')

    if request.method == 'POST':
        department.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('dashboard')

    return render(request, 'partnership/department_delete.html', {'department': department})


@login_required
def department_add_view(request):
    return render(request, 'partnership/department_add.html')

@login_required
def department_delete_view(request, dept_id):
    # Logic can be implemented later
    return render(request, 'partnership/department_delete.html', {'dept_id': dept_id})


# -----------------------------
# DRF ViewSets
# -----------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

# The Department model is defined in partnership.models; the duplicate model
# definition was removed from views.py to avoid importing or referencing
# django.db.models here and to keep models in models.py.