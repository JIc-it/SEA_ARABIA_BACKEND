from .models import *
from django.contrib import admin
from .forms import UpdateUserForm, AddUserForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.site_header = "Sea Arabia Admin"
admin.site.site_title = "Sea Arabia Admin Panel"
admin.site.index_title = "Welcome To Sea Arabia Admin Panel"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = (
        "account_id", "first_name", "last_name", "email", "is_email_verified", "mobile", "role", "is_staff",
        "created_at", "updated_at")
    list_filter = ("role", "is_staff", "is_active", "is_superuser")
    readonly_fields = ["account_id"]
    fieldsets = (
        (None, {"fields": ("email", "password", "is_email_verified", "is_mobile_verified",)}),
        ("Personal info", {"fields": ("account_id", "first_name", "last_name", "mobile", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions",)}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": (
        "first_name", "last_name", "email", "mobile", "role", "password1", "password2",), }))
    search_fields = ("account_id", "first_name", "last_name", "email", "mobile")
    ordering = ("first_name", "email")
    filter_horizontal = ("groups", "user_permissions")

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
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]


@admin.register(UserIdentificationData)
class UserIdentificationDataAdmin(admin.ModelAdmin):
    list_display = ["user", "id_type", "id_number", "is_verified"]
    list_filter = ["id_type", "is_verified", "created_at", "updated_at"]
    search_fields = ["user__email", "user__mobile", "user__first_name", "user__lase_name", "id_number"]


@admin.register(ProfileExtra)
class ProfileExtraAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "dob", "gender"]
    list_filter = ["location", "gender", "created_at", "updated_at"]
    search_fields = ["user__email", "user__mobile", "user__first_name", "user__lase_name", "id_number",
                     "location__country", "location__country_code"]


@admin.register(Bookmark)
class BookMarkAdmin(admin.ModelAdmin):
    list_display = ["user", "service", "created_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user__email", "user__mobile", "user__first_name", "user__lase_name", "service__name"]


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ["guest_id", "first_name", "last_name", "location", "email", "mobile"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["guest_id", "first_name", "last_name", "email", "mobile"]


@admin.register(GCCLocations)
class GCCLocationAdmin(admin.ModelAdmin):
    list_display = ["country", "country_code", "is_active", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["country", "country_code", ]
