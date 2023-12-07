from django.db import models
from local_apps.core.models import Main
from django.conf import settings
from utils.file_handle import remove_file
from local_apps.main.models import Category

COMPANY_STATUS = (
    ("New Lead", "New Lead"),
    ("Initial Contact", "Initial Contact"),
    ("Site Visit", "Site Visit"),
    ("Proposal", "Proposal"),
    ("Negotations", "Negotations"),
    ("MOU/Charter", "MOU/Charter"),
    ("Onboard", "Onboard"),
)


class OnboardStatus(Main):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "OnBoard Status"
        verbose_name_plural = "Onboard Status"


class ServiceTag(Main):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Service Tag"
        verbose_name_plural = "Service Tags"


class Company(Main):
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
    registration_number = models.CharField(max_length=200, blank=True, null=True)
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


class MiscellaneousType(Main):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

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

    def save(self, *args, **kwargs):
        try:
            this_instance = Miscellaneous.objects.get(id=self.id)
            old_file = this_instance.attachment
        except Miscellaneous.DoesNotExist:
            old_file = None

        super(Miscellaneous, self).save(*args, **kwargs)

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        if self.attachment:
            remove_file(self.attachment)

        super(Miscellaneous, self).delete(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        try:
            this_instance = SiteVisit.objects.get(id=self.id)
            old_file = this_instance.attachment
        except SiteVisit.DoesNotExist:
            old_file = None

        super(SiteVisit, self).save(*args, **kwargs)

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        if self.attachment:
            remove_file(self.attachment)

        super(SiteVisit, self).delete(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        try:
            this_instance = Proposal.objects.get(id=self.id)
            old_file = this_instance.attachment
        except Proposal.DoesNotExist:
            old_file = None

        super(Proposal, self).save(*args, **kwargs)

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        if self.attachment:
            remove_file(self.attachment)

        super(Proposal, self).delete(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        try:
            this_instance = Negotiation.objects.get(id=self.id)
            old_file = this_instance.attachment
        except Negotiation.DoesNotExist:
            old_file = None

        super(Negotiation, self).save(*args, **kwargs)

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        if self.attachment:
            remove_file(self.attachment)

        super(Negotiation, self).delete(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        try:
            this_instance = MOUorCharter.objects.get(id=self.id)
            old_file = this_instance.attachment
        except MOUorCharter.DoesNotExist:
            old_file = None

        super(MOUorCharter, self).save(*args, **kwargs)

        if old_file and self.attachment and old_file != self.attachment:
            remove_file(old_file)

    def delete(self, *args, **kwargs):
        if self.attachment:
            remove_file(self.attachment)

        super(MOUorCharter, self).delete(*args, **kwargs)
