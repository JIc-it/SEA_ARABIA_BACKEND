from django.contrib import admin
from .models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Miscellaneous)
class MiscellaneousAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceTag)
class ServiceTagAdmin(admin.ModelAdmin):
    pass


@admin.register(MiscellaneousType)
class MiscellaneousTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    pass


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    pass


@admin.register(Negotiation)
class NegotiationAdmin(admin.ModelAdmin):
    pass


@admin.register(MOUorCharter)
class MOUorCharterAdmin(admin.ModelAdmin):
    pass
