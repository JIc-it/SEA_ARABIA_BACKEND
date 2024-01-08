from datetime import datetime
from django.core.serializers import serialize
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.parsers import MultiPartParser
from utils.action_logs import create_log
from .models import *
from .serializers import *
from .filters import *
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page


#   service CRUD view


class ServiceTagList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = ServiceTag.objects.all()
    serializer_class = ServiceTagSerializer


# Onboard status view

# @method_decorator(cache_page(60 * 15), name='dispatch')
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

# @method_decorator(cache_page(60 * 15), name='dispatch')


class CompanyListCms(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanyCmsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyFilter


class CompanyCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def create(self, request, *args, **kwargs):
        try:
            # Serialize the data before the company creation
            value_before = serialize('json', [Company()])

            response = super().create(request, *args, **kwargs)

            # Get the created company instance
            company = Company.objects.get(pk=response.data['id'])

            # Serialize the data after the company creation
            value_after = serialize('json', [company])

            # Log the company creation action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Company",
                action='Created',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Company',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CompanyView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the company instance before the update
            company_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [company_before_update])

            response = super().update(request, *args, **kwargs)

            # Get the updated company instance
            company_after_update = self.get_object()

            # Serialize the data after the update
            value_after = serialize('json', [company_after_update])

            # Log the company update action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Company",
                action='Updated',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Company',
                action_value='Update',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CompanyActiveUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the company instance before the update
            company_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [company_before_update])

            company = Company.objects.get(pk=kwargs['pk'])
            active_status = request.data.get('status', None)
            if active_status:
                company.is_active = True if active_status == True or active_status == 'True' or active_status == 'true' else False
            company.save()

            # Get the updated company instance
            company_after_update = self.get_object()

            # Serialize the data after the update
            value_after = serialize('json', [company_after_update])

            # Log the company update action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Company",
                action='Updated',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Company',
                action_value='Update',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Miscellaneous Types Views


class MiscellaneousTypeList(generics.ListAPIView):
    queryset = MiscellaneousType.objects.all()
    serializer_class = MiscellaneousTypeSerializer


# Miscellaneous CRUD Views


class MiscellaneousCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Serialize the data before the Miscellaneous creation
            value_before = serialize('json', [Miscellaneous()])

            response = super().create(request, *args, **kwargs)

            # Get the created Miscellaneous instance
            miscellaneous = Miscellaneous.objects.get(pk=response.data['id'])

            # Serialize the data after the Miscellaneous creation
            value_after = serialize('json', [miscellaneous])

            # Log the Miscellaneous creation action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Miscellaneous",
                action='Created',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Miscellaneous',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MiscellaneousList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get("id")
        return Miscellaneous.objects.filter(company=company_id)


class MiscellaneousUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Miscellaneous.objects.all()
    serializer_class = MiscellaneousSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the Miscellaneous instance before the update
            miscellaneous_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [miscellaneous_before_update])

            instance = self.get_object()
            attachment_data = request.data.get('attachment')

            if attachment_data is not None:
                # Handle file upload separately
                instance.attachment = attachment_data
                instance.save(update_fields=['attachment'])

            # Create a mutable copy of the request data
            mutable_data = request.data.copy()

            # Remove 'attachment' from the mutable data to avoid validation issues
            mutable_data.pop('attachment', None)

            serializer = self.get_serializer(
                instance, data=mutable_data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Get the updated Miscellaneous instance
                miscellaneous_after_update = self.get_object()

                # Serialize the data after the update
                value_after = serialize('json', [miscellaneous_after_update])

                # Log the Miscellaneous update action
                log_user = request.user if request.user else 'Unknown User'
                log_title = "{model} entry {action} by {user}".format(
                    model="Miscellaneous",
                    action='Updated',
                    user=log_user
                )

                create_log(
                    user=request.user,
                    model_name='Miscellaneous',
                    action_value='Update',
                    title=log_title,
                    value_before=value_before,
                    value_after=value_after
                )

                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
    parser_classes = [MultiPartParser,]

    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     qualifications = self.request.data.get("qualifications",None)
    #     if qualifications:
    #         instance.qualifications.set(qualifications)
    #     return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        try:

            # Serialize the data before the creation
            value_before = serialize('json', [SiteVisit()])
            qualifications = request.data.get("qualifications", None)
            attachment = request.FILES.get('attachment')
            company = request.data.get('company', None)
            title = request.data.get('title', None)
            note = request.data.get('note', None)
            date_str = request.data.get('date', None)
            time_str = request.data.get('time', None)

            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

            if time_str:
                time = datetime.strptime(time_str, '%H:%M:%S').time()

            if company:
                company_instance = Company.objects.get(id=company)

                site_visit_instance = SiteVisit.objects.create(
                    company=company_instance, attachment=attachment, title=title, note=note, date=date, time=time)
                
                qualifications_list = []  # Initialize qualifications_list as an empty list for cases with no qualification

                if qualifications:
                    qualifications_list = qualifications.split(',')
                    for qualification in qualifications_list:
                        print(qualification, ',,')
                        site_visit_instance.qualifications.add(qualification)
                        # site_visit_instance.qualifications.set(qualifications_list)

                serializer = SiteVisitSerializer(site_visit_instance)

                # Serialize the data after the SiteVisit creation
                value_after = serialize('json', [site_visit_instance])

                # Log the SiteVisit creation action
                log_user = self.request.user if self.request.user else 'Unknown User'
                log_title = "{model} entry {action} by {user}".format(
                    model="SiteVisit",
                    action='Created',
                    user=log_user
                )

                create_log(
                    user=self.request.user,
                    model_name='SiteVisit',
                    action_value='Create',
                    title=log_title,
                    value_before=value_before,
                    value_after=value_after
                )
                serialized_data = serializer.data
                serialized_data['qualifications'] = qualifications_list
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            else:
                return Response("Company id not provided", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class SiteVisitList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get("id")
        return SiteVisit.objects.filter(company=company_id)


class SiteVisitUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the SiteVisit instance before the update
            site_visit_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [site_visit_before_update])

            instance = self.get_object()
            attachment_data = request.data.get('attachment')

            if attachment_data is not None:
                # Handle file upload separately
                instance.attachment = attachment_data
                instance.save(update_fields=['attachment'])

            # Create a mutable copy of the request data
            mutable_data = request.data.copy()

            # Remove 'attachment' from the mutable data to avoid validation issues
            mutable_data.pop('attachment', None)

            serializer = self.get_serializer(
                instance, data=mutable_data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Get the updated SiteVisit instance
                site_visit_after_update = self.get_object()

                # Serialize the data after the update
                value_after = serialize('json', [site_visit_after_update])

                # Log the SiteVisit update action
                log_user = request.user if request.user else 'Unknown User'
                log_title = "{model} entry {action} by {user}".format(
                    model="SiteVisit",
                    action='Updated',
                    user=log_user
                )

                create_log(
                    user=request.user,
                    model_name='SiteVisit',
                    action_value='Update',
                    title=log_title,
                    value_before=value_before,
                    value_after=value_after
                )

                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SiteVisitView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer


# Proposal CRUD Views


class ProposalCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Serialize the data before the Proposal creation
            value_before = serialize('json', [Proposal()])

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            # Serialize the data after the Proposal creation
            value_after = serialize('json', [instance])

            # Log the Proposal creation action
            log_user = self.request.user if self.request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Proposal",
                action='Created',
                user=log_user
            )

            create_log(
                user=self.request.user,
                model_name='Proposal',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ProposalList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get("id")
        return Proposal.objects.filter(company=company_id)


class ProposalUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        attachment_data = request.data.get('attachment')

        if attachment_data is not None:
            # Handle file upload separately
            instance.attachment = attachment_data
            instance.save(update_fields=['attachment'])

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Remove 'attachment' from the mutable data to avoid validation issues
        mutable_data.pop('attachment', None)

        serializer = self.get_serializer(
            instance, data=mutable_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class ProposalView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


# Negotiation CRUD Views


class NegotiationCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer

    def create(self, request, *args, **kwargs):
        try:

            # Serialize the data before the creation
            value_before = serialize('json', [Negotiation()])

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            # Serialize the data after the Negotiation creation
            value_after = serialize('json', [instance])

            # Log the Negotiation creation action
            log_user = self.request.user if self.request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Negotiation",
                action='Created',
                user=log_user
            )

            create_log(
                user=self.request.user,
                model_name='Negotiation',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class NegotiationList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get("id")
        return Negotiation.objects.filter(company=company_id)


class NegotiationUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the Negotiation instance before the update
            negotiation_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [negotiation_before_update])

            instance = self.get_object()
            attachment_data = request.data.get('attachment')

            if attachment_data is not None:
                # Handle file upload separately
                instance.attachment = attachment_data
                instance.save(update_fields=['attachment'])

            # Create a mutable copy of the request data
            mutable_data = request.data.copy()

            # Remove 'attachment' from the mutable data to avoid validation issues
            mutable_data.pop('attachment', None)

            serializer = self.get_serializer(
                instance, data=mutable_data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Get the updated Negotiation instance
                negotiation_after_update = self.get_object()

                # Serialize the data after the update
                value_after = serialize('json', [negotiation_after_update])

                # Log the Negotiation update action
                log_user = request.user if request.user else 'Unknown User'
                log_title = "{model} entry {action} by {user}".format(
                    model="Negotiation",
                    action='Updated',
                    user=log_user
                )

                create_log(
                    user=request.user,
                    model_name='Negotiation',
                    action_value='Update',
                    title=log_title,
                    value_before=value_before,
                    value_after=value_after
                )

                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NegotiationView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer


# MOUorCharter CRUD Views


class MOUorCharterCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer

    def create(self, request, *args, **kwargs):
        try:

            # Serialize the data before the creation
            value_before = serialize('json', [MOUorCharter()])

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            # Serialize the data after the MOUorCharter creation
            value_after = serialize('json', [instance])

            # Log the MOUorCharter creation action
            log_user = self.request.user if self.request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="MOUorCharter",
                action='Created',
                user=log_user
            )

            create_log(
                user=self.request.user,
                model_name='MOUorCharter',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class MOUorCharterList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get("id")
        return MOUorCharter.objects.filter(company=company_id)


class MOUorCharterUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the MOUorCharter instance before the update
            mou_or_charter_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [mou_or_charter_before_update])

            instance = self.get_object()
            attachment_data = request.data.get('attachment')

            if attachment_data is not None:
                # Handle file upload separately
                instance.attachment = attachment_data
                instance.save(update_fields=['attachment'])

            # Create a mutable copy of the request data
            mutable_data = request.data.copy()

            # Remove 'attachment' from the mutable data to avoid validation issues
            mutable_data.pop('attachment', None)

            serializer = self.get_serializer(
                instance, data=mutable_data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Get the updated MOUorCharter instance
                mou_or_charter_after_update = self.get_object()

                # Serialize the data after the update
                value_after = serialize('json', [mou_or_charter_after_update])

                # Log the MOUorCharter update action
                log_user = request.user if request.user else 'Unknown User'
                log_title = "{model} entry {action} by {user}".format(
                    model="MOUorCharter",
                    action='Updated',
                    user=log_user
                )

                create_log(
                    user=request.user,
                    model_name='MOUorCharter',
                    action_value='Update',
                    title=log_title,
                    value_before=value_before,
                    value_after=value_after
                )

                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MOUorCharterView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = MOUorCharter.objects.all()
    serializer_class = MOUorCharterSerializer


#   Onboard vendor views

class OnboardVendor(generics.UpdateAPIView):
    ''' view for onboarding and offloading the vendor based on the status '''

    queryset = Company.objects.all()
    serializer_class = CompanyOnboardSerializer

    def update(self, request, *args, **kwargs):
        try:
            company_id = kwargs.get('pk', None)
            onboard_status = request.data.get('status', None)

            # Get the initial Company instance
            company_instance = get_object_or_404(Company, id=company_id)

            # Serialize the data before the update
            value_before = serialize('json', [company_instance])

            company_instance.is_onboard = onboard_status
            company_instance.save()

            # Get the updated Company instance
            company_after_update = self.get_object()

            # Serialize the data after the update
            value_after = serialize('json', [company_after_update])

            # Log the Company update action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Company",
                action='Updated',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Company',
                action_value='Update',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            serializer_data = CompanyOnboardSerializer(company_after_update)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


# vendor onboarding status

# class ChangeStatusAPIView(generics.UpdateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#
#     def update(self, request, args, *kwargs):
#         instance = self.get_object()
#
#         # Get the status to change from the request parameters
#         updated_status = request.query_params.get('new_status')
#
#         if not updated_status:
#             return Response({'detail': 'Invalid request. Please provide the new_status parameter.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Check if the provided status is valid
#         try:
#             new_status = OnboardStatus.objects.get(name=updated_status)
#         except OnboardStatus.DoesNotExist:
#             return Response({'detail': f'Invalid status: {updated_status}'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Update the status based on the provided parameter
#         if updated_status == "Site Visit" and not User.objects.filter(company=instance).exists():
#             return Response({'detail': 'Invalid operation. Initial Contact does not exist.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         elif updated_status == "Proposal" and not SiteVisit.objects.filter(company=instance).exists():
#             return Response({'detail': 'Invalid operation. Site Visit does not exist.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         elif updated_status == "Negotiation" and not Proposal.objects.filter(company=instance).exists():
#             return Response({'detail': 'Invalid operation. Proposal does not exist.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         elif updated_status == "MOU / Charter" and not Negotiation.objects.filter(company=instance).exists():
#             return Response({'detail': 'Invalid operation. Negotiation does not exist.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         instance.status = new_status
#         instance.save()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


class ChangeStatusAPIView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the Company instance before the update
            company_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [company_before_update])

            instance = self.get_object()

            # Get the status id to change from the request parameters
            updated_status = request.data.get('new_status')

            if not updated_status:
                return Response({'detail': 'Invalid request. Please provide the new_status parameter.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the provided status id is valid
            try:
                new_status = OnboardStatus.objects.get(name=updated_status)
            except OnboardStatus.DoesNotExist:
                return Response({'detail': f'Invalid status: {updated_status}'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Update the status based on the provided parameter
            if updated_status == "Site Visit" and not Company.objects.filter(status__name="Initial Contact"):
                return Response({'detail': 'Invalid operation. Initial Contact does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif updated_status == "Proposal" and not SiteVisit.objects.filter(company=instance).exists():
                return Response({'detail': 'Invalid operation. Site Visit does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif updated_status == "Negotiation" and not Proposal.objects.filter(company=instance).exists():
                return Response({'detail': 'Invalid operation. Proposal does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif updated_status == "MOU / Charter" and not Negotiation.objects.filter(company=instance).exists():
                return Response({'detail': 'Invalid operation. Negotiation does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)

            instance.status = new_status
            instance.save()

            # Get the updated Company instance
            company_after_update = self.get_object()

            # Serialize the data after the update
            value_after = serialize('json', [company_after_update])

            # Log the Company update action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Company",
                action='Updated',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Company',
                action_value='Update',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
