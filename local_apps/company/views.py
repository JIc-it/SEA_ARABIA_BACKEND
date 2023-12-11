from rest_framework import generics,views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import *
from .serializers import *
from .filters import *


#   service CRUD view


class ServiceTagList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = ServiceTag.objects.all()
    serializer_class = ServiceTagSerializer


# Onboard status view


class OnboardStatusList(generics.ListAPIView):
    queryset = OnboardStatus.objects.all().order_by("order")
    serializer_class = OnboardStatusSerializer


# Company CRUD view


class CompanyList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
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


# Miscellaneous Types Views


class MiscellaneousTypeList(generics.ListAPIView):
    queryset = MiscellaneousType.objects.all()
    serializer_class = MiscellaneousTypeSerializer


# Miscellaneous CRUD Views


class MiscellaneousCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


class MiscellaneousList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


class MiscellaneousUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


class MiscellaneousView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer


# Quafification CRUD Views


class QualificationsList(generics.ListAPIView):
    queryset = Qualifications.objects.all()
    serializer_class = QualificationSerializer


# SiteVisit CRUD Views


class SiteVisitCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


class SiteVisitList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


class SiteVisitUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


class SiteVisitView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
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


#   Onboard vendor views

class OnboardVendor(generics.UpdateAPIView):
    ''' view for onboarding and offloading the vendor based on the status '''
    
    queryset = Company.objects.filter(is_onboard = False)
    serializer_class = CompanyOnboardSerializer

    def update(self, request, *args, **kwargs):
        try:
            company_id = kwargs.get('pk',None)
            onboard_status = request.data.get('status',None)
            company_instance = get_object_or_404(Company,id=company_id)
            company_instance.is_onboard = onboard_status
            company_instance.save()
            serializer_data = CompanyOnboardSerializer(self.request.data)
            return Response(serializer_data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}",status= status.HTTP_400_BAD_REQUEST)