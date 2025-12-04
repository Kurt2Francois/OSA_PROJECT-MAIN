from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# -----------------------------
# Initialize DRF router
# -----------------------------
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'departments', views.DepartmentViewSet, basename='department')

# -----------------------------
# Web URL patterns
# -----------------------------
urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    path('department/<int:dept_id>/', views.department_detail_view, name='department_detail'),
    path('department/<int:dept_id>/edit/', views.department_edit_view, name='department_edit'),
    
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('admin-panel/user/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    path('owner-panel/', views.owner_panel_view, name='owner_panel'),
    
    path('owner-panel/department/add/', views.department_add_view, name='department_add'),
    path('owner-panel/department/<int:dept_id>/delete/', views.department_delete_view, name='department_delete'),
    
    # Include DRF API routes at /api/
    path('api/', include(router.urls)),
]
