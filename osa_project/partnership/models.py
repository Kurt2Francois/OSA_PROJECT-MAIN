from django.db import models
from django.contrib.auth.models import User

# User profile to extend default User
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('department', 'Department'),
        ('admin', 'Admin'),
        ('owner', 'Owner'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    business_email = models.EmailField(max_length=255)
    department_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='department')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} ({self.user_type})"


# Department model
class Department(models.Model):
    PARTNERSHIP_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='departments')
    department_name = models.CharField(max_length=255)
    business_email = models.EmailField(max_length=255)
    email = models.EmailField()
    contact_person = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=50, blank=True)
    logo_path = models.ImageField(upload_to='logos/', blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    partnership_status = models.CharField(max_length=20, choices=PARTNERSHIP_STATUS_CHOICES, default='pending')
    remarks_status = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department_name} ({self.business_email})"

    @property
    def status_color(self):
        colors = {'active': 'green', 'inactive': 'red', 'pending': 'orange'}
        return colors.get(self.partnership_status, 'black')
