from django.contrib import admin
from .models import *


@admin.register(MiscellaneousType)
class MiscellaneousTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ['name']


@admin.register(Qualifications)
class QualificationsAdmin(admin.ModelAdmin):
    list_display = ['name', "short_description"]
    search_fields = ['name']


@admin.register(OnboardStatus)
class OnboardStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    search_fields = ['name']

# @admin.register(ServiceTag)
# class ServiceTagAdmin(admin.ModelAdmin):
#     pass


class MiscellaneousAdmin(admin.StackedInline):
    model = Miscellaneous
    extra = 0


class SiteVisitAdmin(admin.StackedInline):
    model = SiteVisit
    extra = 0


class ProposalAdmin(admin.StackedInline):
    model = Proposal
    extra = 0


class NegotiationAdmin(admin.StackedInline):
    model = Negotiation
    extra = 0


class MOUorCharterAdmin(admin.StackedInline):
    model = MOUorCharter
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [MiscellaneousAdmin, SiteVisitAdmin,
               ProposalAdmin, NegotiationAdmin, MOUorCharterAdmin]
    list_display = ["name", 'user', "registration_number",
                    'created_by', "is_onboard", "is_active"]
    search_fields = ['name', 'user__first_name', 'created_by__first_name']
    list_filter = ['is_onboard', "is_active"]
