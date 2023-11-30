from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import *
from .serializers import *
from .filters import *

#   service CRUD view


class ServiceTagList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = ServiceTag.objects.all()
    serializer_class = ServiceTagSerializer


# Company CRUD view


class CompanyList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "name",
        "registration_number",
        "service_summary__name",
    ]
    filterset_class = CompanyFilter


class CompanyCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# Miscellaneous CRUD Views


class MiscellaneousCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


class MiscellaneousList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


class MiscellaneousUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


class MiscellaneousView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


# Quafification CRUD Views


class QualificationsList(generics.ListAPIView):
    queryset = Qualifications.objects.all()
    serializer_class = QualificationSerializer


# SiteVisit CRUD Views


class SiteVisitCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


class SiteVisitList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


class SiteVisitUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


class SiteVisitView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


# Proposal CRUD Views


class ProposalCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


# Negotiation CRUD Views


class NegotiationCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer


class NegotiationList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer


class NegotiationUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer


class NegotiationView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer


# MOUorCharter CRUD Views


class MOUorCharterCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer


class MOUorCharterList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer


class MOUorCharterUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer


class MOUorCharterView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer
