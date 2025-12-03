from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Department, UserProfile

# -----------------------------
# User Serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return {
                'business_name': obj.profile.business_name,
                'department_name': obj.profile.department_name,
                'contact_person': obj.profile.contact_person,
                'contact_number': obj.profile.contact_number,
                'user_type': obj.profile.user_type,
            }
        return {}

# -----------------------------
# User Create Serializer
# -----------------------------
class UserCreateSerializer(serializers.ModelSerializer):
    confirm_email = serializers.EmailField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'confirm_email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['email'] != data['confirm_email']:
            raise serializers.ValidationError({"email": "Email addresses do not match"})
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_email')
        validated_data.pop('confirm_password')
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# -----------------------------
# Department Serializer
# -----------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='owner.email', read_only=True)
    status_color = serializers.CharField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'owner', 'user_email', 'department_name', 'business_name',
                  'email', 'logo_path', 'established_date', 'expiration_date',
                  'partnership_status', 'status_color', 'remarks_status', 'created_at', 'last_updated']
        read_only_fields = ['id', 'created_at', 'last_updated']
