import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import models
from django.contrib.auth.models import AbstractUser
from local_apps.account.managers import CustomUserManager
from local_apps.api_report.models import ModelUpdateLog
from local_apps.core.models import Main
from utils.file_handle import remove_file
from django.utils import timezone
from local_apps.service.models import Service
from django.conf import settings
from local_apps.api_report.middleware import get_current_request
from django.core.exceptions import ValidationError
from utils.id_handle import increment_two_digits, increment_two_letters, increment_one_letter


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
    prefix = models.CharField(max_length=10, default="SA")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    account_id = models.CharField(max_length=220)
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

    def generate_id_number(self):
        last_entry = User.objects.order_by('-created_at').first()
        if self.role == 'Admin':
            rle = 'ADM'
        elif self.role == 'Staff':
            rle = 'STF'
        elif self.role == 'Vendor':
            rle = 'VDR'
        elif self.role == 'User':
            rle = 'USR'
        else:
            rle = 'OTH'

        if last_entry:
            if last_entry.last_two_numbers == 99:
                self.last_one_letter = increment_one_letter(last_entry.last_one_letter)
            else:
                self.last_one_letter = last_entry.last_one_letter

            if last_entry.last_one_letter in ['Z', 'z'] and last_entry.last_two_numbers == 99:
                self.first_two_numbers = increment_two_digits(last_entry.first_two_numbers)
            else:
                self.first_two_numbers = last_entry.first_two_numbers

            if last_entry.first_two_numbers == 99 and last_entry.last_one_letter in ['Z',
                                                                                     'z'] and last_entry.last_two_numbers == 99:
                self.first_two_letters = increment_two_letters(last_entry.first_two_letters)
            else:
                self.first_two_letters = last_entry.first_two_letters

            self.last_two_numbers = increment_two_digits(last_entry.last_two_numbers)

            self.account_id = f"{self.prefix}-{rle}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.account_id = f"{self.prefix}-{rle}-AA00A00"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            # user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        if not self.account_id:
            self.generate_id_number()

        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [User.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(User, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(User, self).save(*args, **kwargs)
  
    # def save(self, *args, **kwargs):
    #     if not self.account_id:
    #         self.generate_id_number()
    #     super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    # if not self.account_id:
    #     self.generate_id_number()
    # super().save(*args, **kwargs)


class GCCLocations(Main):
    location = models.CharField(max_length=255, null=True, blank=True)
    country_flag = models.ImageField(
        upload_to="account/gcclocations/country_flag", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.location if self.location else "No Location"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [GCCLocations.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(GCCLocations, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(GCCLocations, self).save(*args, **kwargs)


class ProfileExtra(Main):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(
        GCCLocations, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='account/profile_extra/image', blank=True, null=True)
    dob = models.DateField(blank=True, null=True, max_length=255)
    gender = models.CharField(
        choices=GENDER, max_length=100, default='Male', blank=True, null=True)

    def __str__(self):
        return self.user.email if self.user and self.user.email else 'No user'

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            # user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [ProfileExtra.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(ProfileExtra, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(ProfileExtra, self).save(*args, **kwargs)

        # Remove old image if it has changed
        try:
            this_instance = ProfileExtra.objects.get(id=self.id)
            old_image = this_instance.image
        except ProfileExtra.DoesNotExist:
            old_image = None

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        # Remove image before deleting the instance
        if self.image:
            remove_file(self.image)

        super(ProfileExtra, self).delete(*args, **kwargs)
        self.create_update_log(data_before, None)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Profile Extra'
        verbose_name_plural = 'Profile Extra'


class UserIdentificationType(Main):
    name = models.CharField(max_length=255)

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [UserIdentificationType.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(UserIdentificationType, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(UserIdentificationType, self).save(*args, **kwargs)

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

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [UserIdentificationData.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(UserIdentificationData, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(UserIdentificationData, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        if self.image:
            remove_file(self.image)

        super(UserIdentificationData, self).delete(*args, **kwargs)
        # Create a log entry after deletion
        self.create_update_log(data_before, None)

    def __str__(self):
        return self.id_number if self.id_number else 'no id number'

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

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [PasswordReset.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(PasswordReset, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(PasswordReset, self).save(*args, **kwargs)

    def __str__(self):
        return f"PasswordReset for {self.user.email}"


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

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [Bookmark.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Bookmark, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Bookmark, self).save(*args, **kwargs)


class Guest(Main):
    """ Guest User Model """

    # ID handling section
    prefix = models.CharField(max_length=10, default="SA-GST")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    guest_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
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

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [Guest.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Guest, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Guest, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Guest User"
        verbose_name_plural = "Guest Users"

    def generate_id_number(self):
        last_entry = Guest.objects.order_by('-created_at').first()
        if last_entry:
            if last_entry.last_two_numbers == 99:
                self.last_one_letter = increment_one_letter(last_entry.last_one_letter)
            else:
                self.last_one_letter = last_entry.last_one_letter

            if last_entry.last_one_letter in ['Z', 'z'] and last_entry.last_two_numbers == 99:
                self.first_two_numbers = increment_two_digits(last_entry.first_two_numbers)
            else:
                self.first_two_numbers = last_entry.first_two_numbers

            if last_entry.first_two_numbers == 99 and last_entry.last_one_letter in ['Z',
                                                                                     'z'] and last_entry.last_two_numbers == 99:
                self.first_two_letters = increment_two_letters(last_entry.first_two_letters)
            else:
                self.first_two_letters = last_entry.first_two_letters

            self.last_two_numbers = increment_two_digits(last_entry.last_two_numbers)

            self.guest_id = f"{self.prefix}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.guest_id = f"{self.prefix}-AA00A00"

    def save(self, *args, **kwargs):
        if not self.guest_id:
            self.generate_id_number()
        super(Guest, self).save(*args, **kwargs)
