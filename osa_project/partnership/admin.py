from django.contrib import admin
from .models import UserProfile, Department

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'department_name', 'contact_person', 'user_type', 'created_at']
    list_filter = ['user_type', 'user__is_active', 'created_at']
    search_fields = ['user__email', 'business_name', 'department_name', 'contact_person']
    readonly_fields = ['created_at']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type', 'user__is_active')
        }),
        ('Business Information', {
            'fields': ('business_name', 'department_name', 'contact_person', 'contact_number')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'department_name', 'business_name', 'email', 'partnership_status', 'established_date', 'expiration_date', 'owner']
    list_filter = ['partnership_status', 'established_date']
    search_fields = ['department_name', 'business_name', 'email', 'owner__email']
    readonly_fields = ['created_at', 'last_updated']

    fieldsets = (
        ('Department Information', {
            'fields': ('owner', 'department_name', 'business_name', 'email', 'contact_person', 'contact_number')
        }),
        ('Partnership Details', {
            'fields': ('logo_path', 'established_date', 'expiration_date', 'partnership_status', 'remarks_status')
        }),
        ('Metadata', {
            'fields': ('created_at', 'last_updated')
        }),
    )
