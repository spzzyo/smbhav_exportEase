from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# # Register your models here.
# admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser.
    Ensures password hashing and proper handling of fields.
    """
    model = CustomUser
    list_display = ("username", "email", "user_type", "is_staff", "is_active")
    list_filter = ("user_type", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("User Type", {"fields": ("user_type",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "user_type", "is_staff", "is_active"),
        }),
    )
    search_fields = ("username", "email")
    ordering = ("username",)

    def save_model(self, request, obj, form, change):
        """
        Ensures that the password is properly hashed before saving the user.
        """
        if not change:  # New user
            obj.set_password(obj.password)
        elif 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)