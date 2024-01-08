from django.urls import path
from .views import *

urlpatterns = [
    # ServiceTag urls
    path("service-tag-list", ServiceTagList.as_view(), name="service-tag-list"),
    # OrderStatus urls
    path("order-status-list", OnboardStatusList.as_view(), name="order-status-list"),
    # Company urls
    path("company-list/", CompanyList.as_view(), name="company-details-list"),
    path("company-create/", CompanyCreate.as_view(), name="company-details-create"),
    path("company-view/<uuid:pk>", CompanyView.as_view(), name="company-details-view"),
    path("company-update/<uuid:pk>", CompanyUpdate.as_view(), name="company-details-update"),
    path("company-active-update/<uuid:pk>", CompanyActiveUpdate.as_view(), name="company-active-update"),

    # Miscellaneous urls
    path("miscellaneous-type-list", MiscellaneousTypeList.as_view(), name="miscellaneous-type-list"),
    path("miscellaneous-list/", MiscellaneousList.as_view(), name="miscellaneous-list"),
    path("miscellaneous-create/", MiscellaneousCreate.as_view(), name="miscellaneous-create", ),
    path("miscellaneous-view/<uuid:pk>", MiscellaneousView.as_view(), name="miscellaneous-view", ),
    path("miscellaneous-update/<uuid:pk>", MiscellaneousUpdate.as_view(), name="miscellaneous-update", ),

    # Qualifications list
    path("qualification-list", QualificationsList.as_view(), name="qualification-list"),
    # SiteVisit urls
    path("site-visit-list/", SiteVisitList.as_view(), name="site-visit-list"),
    path("site-visit-create/", SiteVisitCreate.as_view(), name="site-visit-create"),
    path("site-visit-view/<uuid:pk>", SiteVisitView.as_view(), name="site-visit-view"),
    path("site-visit-update/<uuid:pk>", SiteVisitUpdate.as_view(), name="site-visit-update"),

    # Proposal urls
    path("proposal-list/", ProposalList.as_view(), name="proposal-list"),
    path("proposal-create/", ProposalCreate.as_view(), name="proposal-create"),
    path("proposal-view/<uuid:pk>", ProposalView.as_view(), name="proposal-view"),
    path("proposal-update/<uuid:pk>", ProposalUpdate.as_view(), name="proposal-update"),

    # Negotiation urls
    path("negotiation-list/", NegotiationList.as_view(), name="negotiation-list"),
    path("negotiation-create/", NegotiationCreate.as_view(), name="negotiation-create"),
    path("negotiation-view/<uuid:pk>", NegotiationView.as_view(), name="negotiation-view"),
    path("negotiation-update/<uuid:pk>", NegotiationUpdate.as_view(), name="negotiation-update", ),

    # MOUorCharter urls
    path("mou-list/", MOUorCharterList.as_view(), name="mou-list"),
    path("mou-create/", MOUorCharterCreate.as_view(), name="mou-create"),
    path("mou-view/<uuid:pk>", MOUorCharterView.as_view(), name="mou-view"),
    path("mou-update/<uuid:pk>", MOUorCharterUpdate.as_view(), name="mou-update"),

    # Onboard Urls
    path("onboard-vendor/<uuid:pk>", OnboardVendor.as_view(), name="onboard-vendor"),
    path("company-cms-list", CompanyListCms.as_view(), name="company-cms-list"),
    path("change-status/<uuid:pk>", ChangeStatusAPIView.as_view(), name="change-status"),
]
