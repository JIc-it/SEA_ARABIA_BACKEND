from .models import *
from django.contrib import admin
from .forms import UpdateUserForm, AddUserForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = (
        "account_id",
        "first_name",
        "last_name",
        "email",
        "is_email_verified",
        "mobile",
        "role",
        "is_staff",
        "created_at",
        "updated_at",
    )
    list_filter = ("role", "is_staff", "is_email_verified")
    readonly_fields = ["account_id"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "is_email_verified",
                    "is_mobile_verified",
             
                )
            },
        ),
        (
            "Personal info",
            {"fields": ("account_id", "first_name", "last_name", "mobile", "role")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "mobile",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("account_id", "first_name", "last_name", "email", "mobile")
    ordering = ("first_name", "email")
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is not None:
            defaults["form"] = UpdateUserForm
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def password_changed(self, request, user, password):
        """
        Called after the user's password has been successfully changed.
        """
        # Customize any additional behavior after the password is changed
        pass


@admin.register(UserIdentificationType)
class UserIdentificationTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["created_at", "updated_at"]


@admin.register(UserIdentificationData)
class UserIdentificationDataAdmin(admin.ModelAdmin):
    list_display = ["user", "id_type", "id_number", "is_verified"]
    list_filter = ["id_type", "is_verified", "created_at", "updated_at"]


@admin.register(ProfileExtra)
class ProfileExtraAdmin(admin.ModelAdmin):
    pass


@admin.register(Bookmark)
class BookMarkAdmin(admin.ModelAdmin):
    list_display = ["user","service"]
    pass
