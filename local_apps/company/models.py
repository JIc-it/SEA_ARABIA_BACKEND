from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import models
from django.utils import timezone

from local_apps.api_report.middleware import get_current_request
from local_apps.api_report.models import ModelUpdateLog
from local_apps.core.models import Main
from django.conf import settings
from utils.file_handle import remove_file
from local_apps.main.models import Category
from django.core.exceptions import ValidationError
from utils.id_handle import increment_two_digits, increment_two_letters, increment_one_letter


COMPANY_STATUS = (
    ("New Lead", "New Lead"),
    ("Initial Contact", "Initial Contact"),
    ("Site Visit", "Site Visit"),
    ("Proposal", "Proposal"),
    ("Negotations", "Negotations"),
    ("MOU/Charter", "MOU/Charter"),
    ("Ready to Onboard", "Ready to Onboard"),
)


class OnboardStatus(Main):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0, unique=True)

    def __str__(self):
        return self.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [OnboardStatus.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(OnboardStatus, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(OnboardStatus, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "OnBoard Status"
        verbose_name_plural = "Onboard Status"


class ServiceTag(Main):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [ServiceTag.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(ServiceTag, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(ServiceTag, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Service Tag"
        verbose_name_plural = "Service Tags"


class Company(Main):
    prefix = models.CharField(max_length=10, default="SA-COM")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    company_id = models.CharField(max_length=255, blank=True, null=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_company_user",
    )
    staffs = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    is_onboard = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="company_company_assigned_to",
    )
    name = models.CharField(max_length=200, blank=True, null=True)
    registration_number = models.CharField(
        max_length=200, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    service_summary = models.ManyToManyField(Category, blank=True)
    # status = models.CharField(
    #     choices=COMPANY_STATUS, default="New Lead", max_length=100
    # )
    status = models.ForeignKey(
        OnboardStatus,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="company_company_status",
    )
    third_party_ownership = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name if self.name else "No Company Name"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def generate_id_number(self):
        last_entry = Company.objects.order_by('-created_at').first()
        if last_entry:
            if last_entry.last_two_numbers == 99:
                self.last_one_letter = increment_one_letter(
                    last_entry.last_one_letter)
            else:
                self.last_one_letter = last_entry.last_one_letter

            if last_entry.last_one_letter in ['Z', 'z'] and last_entry.last_two_numbers == 99:
                self.first_two_numbers = increment_two_digits(
                    last_entry.first_two_numbers)
            else:
                self.first_two_numbers = last_entry.first_two_numbers

            if last_entry.first_two_numbers == 99 and last_entry.last_one_letter in ['Z',
                                                                                     'z'] and last_entry.last_two_numbers == 99:
                self.first_two_letters = increment_two_letters(
                    last_entry.first_two_letters)
            else:
                self.first_two_letters = last_entry.first_two_letters

            self.last_two_numbers = increment_two_digits(
                last_entry.last_two_numbers)

            self.company_id = f"{self.prefix}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.company_id = f"{self.prefix}-AA00A00"

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [Company.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            if not self.company_id:  # for creating new company Id
                self.generate_id_number()

            # Call the original save method to save the instance
            super(Company, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Company, self).save(*args, **kwargs)


class MiscellaneousType(Main):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [MiscellaneousType.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(MiscellaneousType, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(MiscellaneousType, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Miscellaneous Type"
        verbose_name_plural = "Miscellaneous Types"


class Miscellaneous(Main):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_miscellaneous_company"
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    type = models.ManyToManyField(MiscellaneousType, blank=True)
    attachment = models.FileField(
        upload_to="company/miscellaneous/attachment", blank=True, null=True
    )
    note = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Miscellaneous"
        verbose_name_plural = "Miscellaneous"

    def __str__(self):
        return self.title if self.title else "No Title"

    def create_update_log(self, data_before, data_after):
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=self.user,  # Assuming there is a user field in your Miscellaneous model
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            # Get the data before the update
            data_before = serialize(
                'json', [Miscellaneous.objects.get(pk=self.pk)]) or None

            # Call the original save method to save the instance
            super(Miscellaneous, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            super(Miscellaneous, self).save(*args, **kwargs)

        try:
            this_instance = Miscellaneous.objects.get(id=self.id)
            old_file = this_instance.attachment
        except Miscellaneous.DoesNotExist:
            old_file = None

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion

        if self.attachment:
            remove_file(self.attachment)

        super(Miscellaneous, self).delete(*args, **kwargs)

        # Create a log entry after deletion
        self.create_update_log(data_before, None)


class Qualifications(Main):
    name = models.CharField(max_length=255, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    icon = models.ImageField(
        upload_to="company/qualifications/icon", null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Qualification"
        verbose_name_plural = "Qualifications"

    def __str__(self):
        return self.name if self.name else "No Name"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [Qualifications.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Qualifications, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Qualifications, self).save(*args, **kwargs)


class SiteVisit(Main):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_site_visit_company"
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    attachment = models.FileField(
        upload_to="company/site_visit/attachment", blank=True, null=True
    )
    qualifications = models.ManyToManyField(Qualifications, blank=True)
    note = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Site Visit"
        verbose_name_plural = "Site Visits"

    def __str__(self):
        return self.title if self.title else "No Title"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            # Get the data before the update
            try:
                data_before = serialize('json', [SiteVisit.objects.get(pk=self.pk)])
            except SiteVisit.DoesNotExist:
                data_before = None

            # Call the original save method to save the instance
            super(SiteVisit, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            super(SiteVisit, self).save(*args, **kwargs)

        try:
            this_instance = SiteVisit.objects.get(id=self.id)
            old_file = this_instance.attachment
        except SiteVisit.DoesNotExist:
            old_file = None

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion

        if self.attachment:
            remove_file(self.attachment)

        super(SiteVisit, self).delete(*args, **kwargs)

        # Create a log entry after deletion
        self.create_update_log(data_before, None)


class Proposal(Main):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_proposal_company"
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    attachment = models.FileField(
        upload_to="company/proposal/attachment", blank=True, null=True
    )
    note = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Proposal"
        verbose_name_plural = "Proposals"

    def __str__(self):
        return self.title if self.title else "No Title"

    def create_update_log(self, data_before, data_after):
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=self.user,  # Assuming there is a user field in your Proposal model
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            # Get the data before the update
            data_before = serialize(
                'json', [Proposal.objects.get(pk=self.pk)]) or None

            # Call the original save method to save the instance
            super(Proposal, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            super(Proposal, self).save(*args, **kwargs)

        try:
            this_instance = Proposal.objects.get(id=self.id)
            old_file = this_instance.attachment
        except Proposal.DoesNotExist:
            old_file = None

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion

        if self.attachment:
            remove_file(self.attachment)

        super(Proposal, self).delete(*args, **kwargs)

        # Create a log entry after deletion
        self.create_update_log(data_before, None)


class Negotiation(Main):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_negotiation_company"
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    attachment = models.FileField(
        upload_to="company/negotiation/attachment", blank=True, null=True
    )
    note = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Negotiation"
        verbose_name_plural = "Negotiations"

    def __str__(self):
        return self.title if self.title else "No Title"

    def create_update_log(self, data_before, data_after):
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=self.user,  # Assuming there is a user field in your Negotiation model
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            # Get the data before the update
            data_before = serialize(
                'json', [Negotiation.objects.get(pk=self.pk)]) or None

            # Call the original save method to save the instance
            super(Negotiation, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            super(Negotiation, self).save(*args, **kwargs)

        try:
            this_instance = Negotiation.objects.get(id=self.id)
            old_file = this_instance.attachment
        except Negotiation.DoesNotExist:
            old_file = None

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion

        if self.attachment:
            remove_file(self.attachment)

        super(Negotiation, self).delete(*args, **kwargs)

        # Create a log entry after deletion
        self.create_update_log(data_before, None)


class MOUorCharter(Main):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_mou_or_charter_company"
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    attachment = models.FileField(
        upload_to="company/mou_or_charter/attachment", blank=True, null=True
    )
    note = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "MOUorCharter"
        verbose_name_plural = "MOUorCharter"

    def __str__(self):
        return self.title if self.title else "No Title"

    def create_update_log(self, data_before, data_after):
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=self.user,  # Assuming there is a user field in your MOUorCharter model
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            # Get the data before the update
            data_before = serialize(
                'json', [MOUorCharter.objects.get(pk=self.pk)]) or None

            # Call the original save method to save the instance
            super(MOUorCharter, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            super(MOUorCharter, self).save(*args, **kwargs)

        try:
            this_instance = MOUorCharter.objects.get(id=self.id)
            old_file = this_instance.attachment
        except MOUorCharter.DoesNotExist:
            old_file = None

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion

        if self.attachment:
            remove_file(self.attachment)

        super(MOUorCharter, self).delete(*args, **kwargs)

        # Create a log entry after deletion
        self.create_update_log(data_before, None)
