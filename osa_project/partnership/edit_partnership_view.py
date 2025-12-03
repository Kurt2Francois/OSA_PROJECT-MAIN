from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department

def edit_department_view(request, department_id):
    """Edit department information"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    department = get_object_or_404(Department, department_id=department_id)
    
    # Check permissions
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')
    
    if user_role != 'admin' and department.user.user_id != user_id:
        messages.error(request, 'You do not have permission to edit this department')
        return redirect('dashboard')
    
    if request.method == 'POST':
        department.department_name = request.POST.get('department_name')
        department.business_name = request.POST.get('business_name')
        department.email = request.POST.get('email')
        department.established_date = request.POST.get('established_date')
        department.expiration_date = request.POST.get('expiration_date')
        department.partnership_status = request.POST.get('partnership_status')
        department.remarks_status = request.POST.get('remarks_status')
        
        # Handle logo upload
        if 'logo' in request.FILES:
            department.logo = request.FILES['logo']
        
        department.save()
        messages.success(request, 'Department updated successfully!')
        return redirect('department_info', department_id=department_id)
    
    context = {
        'department': department,
        'user_role': user_role
    }
    return render(request, 'edit_department.html', context)