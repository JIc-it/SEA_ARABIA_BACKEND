from django.urls import path
from .views import *

urlpatterns = [
    #   ServiceTag urls
    path("servicetag-list", ServiceTagList.as_view(), name="servicetag-list"),
    #   OrderStatus urls
    path("orderstatus-list", OnboardStatusList.as_view(), name="orderstatus-list"),
    #   Company urls
    path("company-list/", CompanyList.as_view(), name="companydetails-list"),
    path("company-create/", CompanyCreate.as_view(),
         name="companydetails-create"),
    path("company-view/<uuid:pk>", CompanyView.as_view(),
         name="companydetails-view"),
    path("company-update/<uuid:pk>", CompanyUpdate.as_view(),
         name="companydetails-update"),

    path("company-active-update/<uuid:pk>", CompanyActiveUpdate.as_view(), name="company-active-update"),

    #   Miscellaneous urls
    path(
        "miscellaneoustype-list", MiscellaneousTypeList.as_view(), name="miscellaneoustype-list"),
    path("miscellaneous-list/", MiscellaneousList.as_view(),
         name="miscellaneous-list"),
    path("miscellaneous-create/", MiscellaneousCreate.as_view(),
         name="miscellaneous-create", ),
    path("miscellaneous-view/<uuid:pk>",
         MiscellaneousView.as_view(), name="miscellaneous-view", ),
    path("miscellaneous-update/<uuid:pk>",
         MiscellaneousUpdate.as_view(), name="miscellaneous-update", ),

    # qualifications list
    path("qualification-list", QualificationsList.as_view(),
         name="qualification-list"),
    # SiteVisit urls
    path("sitevisit-list/", SiteVisitList.as_view(), name="sitevisit-list"),
    path("sitevisit-create/", SiteVisitCreate.as_view(), name="sitevisit-create"),
    path("sitevisit-view/<uuid:pk>",
         SiteVisitView.as_view(), name="sitevisit-view"),
    path(
        "sitevisit-update/<uuid:pk>", SiteVisitUpdate.as_view(), name="sitevisit-update"
    ),
    # Proposal urls
    path("proposal-list/", ProposalList.as_view(), name="proposal-list"),
    path("proposal-create/", ProposalCreate.as_view(), name="proposal-create"),
    path("proposal-view/<uuid:pk>", ProposalView.as_view(), name="proposal-view"),
    path("proposal-update/<uuid:pk>",
         ProposalUpdate.as_view(), name="proposal-update"),
    # Negotiation urls
    path("negotation-list/", NegotiationList.as_view(), name="negotation-list"),
    path("negotation-create/", NegotiationCreate.as_view(),
         name="negotation-create"),
    path("negotation-view/<uuid:pk>",
         NegotiationView.as_view(), name="negotation-view"),
    path("negotation-update/<uuid:pk>",
         NegotiationUpdate.as_view(), name="negotation-update", ),
    # MOUorCharter urls
    path("mou-list/", MOUorCharterList.as_view(), name="mou-list"),
    path("mou-create/", MOUorCharterCreate.as_view(), name="mou-create"),
    path("mou-view/<uuid:pk>", MOUorCharterView.as_view(), name="mou-view"),
    path("mou-update/<uuid:pk>", MOUorCharterUpdate.as_view(), name="mou-update"),

    # Onboard Urls

    path("onboard-vendor/<uuid:pk>",
         OnboardVendor.as_view(), name="onboard-vendor"),

    path("companycms-list", CompanyListCms.as_view(), name="companycms-list"),

    path("change-status/<uuid:pk>", ChangeStatusAPIView.as_view(), name="change-status"),
]
