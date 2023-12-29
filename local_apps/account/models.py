import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from local_apps.account.managers import CustomUserManager
from local_apps.core.models import Main
from utils.file_handle import remove_file
from django.utils import timezone
from local_apps.service.models import Service
from django.conf import settings


USER_ROLE = (
    ('Admin', "Admin"),
    ('Staff', "Staff"),
    ("Vendor", "Vendor"),
    ("User", "User"),
    ("Others", "Others"),
)

GENDER = (
    ('Male', "Male"),
    ('Female', "Female"),
)


class User(AbstractUser):
    username = None
    date_joined = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.CharField(max_length=20, unique=True)
    account_id_count = models.IntegerField(default=0, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, max_length=200,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    is_email_verified = models.BooleanField(default=False)
    mobile = models.CharField(max_length=20, unique=True, blank=True, null=True,
                              error_messages={
                                  'unique': "A user with that mobile already exists.",
                              })
    is_mobile_verified = models.BooleanField(default=False)
    role = models.CharField(choices=USER_ROLE, max_length=100, default='Others',
                            help_text='ID generation depends on the role. Once you submit it will be permanent.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = CustomUserManager()

    ordering = ["-created_at", "-updated_at"]

    def save(self, *args, **kwargs):
        if not self.account_id:
            last_usr_instance = User.objects.order_by(
                '-account_id_count').first()
            if last_usr_instance:
                self.account_id_count = last_usr_instance.account_id_count + 1
            else:
                self.account_id_count = 1
            if self.role == 'Admin':
                self.account_id = 'SA-ADM-00' + str(self.account_id_count)
            elif self.role == 'Staff':
                self.account_id = 'SA-STF-00' + str(self.account_id_count)
            elif self.role == 'Vendor':
                self.account_id = 'SA-VDR-00' + str(self.account_id_count)
            elif self.role == 'User':
                self.account_id = 'SA-USR-00' + str(self.account_id_count)
            else:
                self.account_id = 'SA-OTH-00' + str(self.account_id_count)
        super(User, self).save(*args, **kwargs)


class ProfileExtra(Main):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(
        upload_to='account/profile_extra/image', blank=True, null=True)
    dob = models.DateField(blank=True, null=True, max_length=255)
    gender = models.CharField(
        choices=GENDER, max_length=100, default='Male', blank=True, null=True)

    def __str__(self):
        return self.user.email if self.user and self.user.email else 'No user'

    def save(self, *args, **kwargs):
        try:
            this_instance = ProfileExtra.objects.get(id=self.id)
            old_image = this_instance.image
        except ProfileExtra.DoesNotExist:
            old_image = None

        super(ProfileExtra, self).save(*args, **kwargs)

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        if self.image:
            remove_file(self.image)

        super(ProfileExtra, self).delete(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Profile Extra'
        verbose_name_plural = 'Profile Extra'


class UserIdentificationType(Main):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'User Identification Type'
        verbose_name_plural = 'User Identification Type'


class UserIdentificationData(Main):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    id_type = models.ForeignKey(
        UserIdentificationType, on_delete=models.SET_NULL, blank=True, null=True)
    id_number = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(
        upload_to='account/user_identification_data/image', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.id_number if self.id_number else 'no id number'

    def save(self, *args, **kwargs):
        try:
            this_instance = UserIdentificationData.objects.get(id=self.id)
            old_image = this_instance.image
        except UserIdentificationData.DoesNotExist:
            old_image = None

        super(UserIdentificationData, self).save(*args, **kwargs)

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        if self.image:
            remove_file(self.image)

        super(UserIdentificationData, self).delete(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'User Identification Data'
        verbose_name_plural = 'User Identification Datas'


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(minutes=5))

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at


class Bookmark(Main):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="account_bookmark_user",
    )
    service = models.ForeignKey(Service, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name='account_bookmark_service')
    def __str__(self):
        return str(self.user)


class Guest(Main):
    """ Guest User Model """
    first_name = models.CharField(
        max_length=255, null=True, blank=True, default="-")
    last_name = models.CharField(
        max_length=255, null=True, blank=True, default="-")
    location = models.CharField(
        max_length=255, null=True, blank=True, default="-")
    mobile = models.CharField(
        max_length=20, null=True, blank=True, default='-')
    email = models.EmailField(
        max_length=255, null=True, blank=True, default="-")

    def __str__(self):
        return self.first_name if self.first_name else "No Name"

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Guest User"
        verbose_name_plural = "Guest Users"
