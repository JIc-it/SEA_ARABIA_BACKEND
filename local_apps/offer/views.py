from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# Create your views here.
from rest_framework import generics, status

from utils.action_logs import create_log
from .models import Offer
from .serializers import OfferSerializer, OfferServiceInfoSerializer, OfferCountSerializer, OfferListExportResource
from rest_framework.response import Response
from local_apps.service.models import Service
from local_apps.company.models import Company
from rest_framework.views import APIView
from .filters import OfferFilter
from django.utils import timezone


class AdminOfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = [
        "name",
        "coupon_code",
    ]
    filterset_class = OfferFilter


class BeastDealsOfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OfferFilter

    def get_queryset(self):
        try:
        
            current_datetime = timezone.now()

            queryset = Offer.objects.filter(is_enable=True, start_date__lte=current_datetime,on_home_screen=True)
           
            queryset = queryset.exclude(end_date__lt=current_datetime)

            return queryset
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OfferCreateView(generics.CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Get the Offer instance before the creation
            offer_before_creation = Offer()  # Create an empty Offer instance

            # Serialize the data before the creation
            value_before = serialize('json', [offer_before_creation])

            is_enable = request.data.get('is_enable', False)
            name = request.data.get('name', None)
            coupon_code = request.data.get('coupon_code', None)
            image = request.FILES.get('image', None)
            discount_type = request.data.get('discount_type', None)
            discount_value = request.data.get('discount_value', None)
            up_to_amount = request.data.get('up_to_amount', None)
            redemption_type = request.data.get('redemption_type', None)
            specify_no = request.data.get('specify_no', None)
            purchase_requirement = request.data.get('purchase_requirement', False)
            min_purchase_amount = request.data.get('min_purchase_amount', None)
            allow_multiple_redeem = request.data.get('allow_multiple_redeem', None)
            multiple_redeem_specify_no = request.data.get('multiple_redeem_specify_no', None)
            on_home_screen = request.data.get('on_home_screen', False)
            on_checkout = request.data.get('on_checkout', False)
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)
            is_lifetime = request.data.get('is_lifetime', False)
            services = request.data.get('services', None)
            companies = request.data.get('companies', None)
            apply_global = request.data.get('apply_global', False)

            try:
                if services:
                    services = services.replace(" ", "")
                    services = services.split(',')
                    if services:
                        services = Service.objects.filter(id__in=services) if Service.objects.filter(
                            id__in=services).exists() else None
                else:
                    services = None

            except Service.DoesNotExist:
                services = None

            try:
                if companies:
                    companies = companies.replace(" ", "")
                    companies = companies.split(',')
                    companies = Company.objects.filter(id__in=companies) if Company.objects.filter(
                        id__in=companies).exists() else None
                else:
                    companies = None
            except Company.DoesNotExist:
                companies = None

            offer = Offer.objects.create(
                is_enable=True if is_enable == 'true' or is_enable == 'True' or is_enable == True else False,
                name=name,
                coupon_code=coupon_code,
                image=image,
                discount_type=discount_type,
                discount_value=discount_value,
                up_to_amount=up_to_amount,
                redemption_type=redemption_type,
                specify_no=specify_no,
                purchase_requirement=True if purchase_requirement == 'true' or purchase_requirement == 'True' or purchase_requirement == True else False,
                min_purchase_amount=min_purchase_amount,
                allow_multiple_redeem=allow_multiple_redeem,
                multiple_redeem_specify_no=multiple_redeem_specify_no,
                on_home_screen=True if on_home_screen == 'true' or on_home_screen == 'True' or on_home_screen == True else False,
                on_checkout=True if on_checkout == 'true' or on_checkout == 'True' or on_checkout == True else False,
                start_date=start_date,
                end_date=end_date,
                is_lifetime=is_lifetime,
                apply_global=True if apply_global == 'true' or apply_global == 'True' or apply_global == True else False)
            if services:
                offer.services.set(services)
            if companies:
                offer.companies.set(companies)
            offer.save()

            # Get the created Offer instance
            offer_after_creation = Offer.objects.filter(id=offer.id).first()

            # Serialize the data after the creation
            value_after = serialize('json', [offer_after_creation])

            # Log the Offer create action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Offer",
                action='Created',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Offer',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            serializer = OfferSerializer(offer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OfferRetrieveView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the Offer instance before the update
            offer_before_update = Offer.objects.get(pk=kwargs['pk'])

            # Serialize the data before the update
            value_before = serialize('json', [offer_before_update])

            offer = Offer.objects.get(pk=kwargs['pk'])

            is_enable = request.data.get('is_enable', False)
            name = request.data.get('name', None)
            coupon_code = request.data.get('coupon_code', None)
            image = request.FILES.get('image', None)
            discount_type = request.data.get('discount_type', None)
            discount_value = request.data.get('discount_value', None)
            up_to_amount = request.data.get('up_to_amount', None)
            redemption_type = request.data.get('redemption_type', None)
            specify_no = request.data.get('specify_no', None)
            purchase_requirement = request.data.get('purchase_requirement', False)
            min_purchase_amount = request.data.get('min_purchase_amount', None)
            allow_multiple_redeem = request.data.get('allow_multiple_redeem', None)
            multiple_redeem_specify_no = request.data.get('multiple_redeem_specify_no', None)
            on_home_screen = request.data.get('on_home_screen', False)
            on_checkout = request.data.get('on_checkout', False)
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)
            is_lifetime = request.data.get('is_lifetime', False)
            services = request.data.get('services', None)
            companies = request.data.get('companies', None)
            apply_global = request.data.get('apply_global', False)

            try:
                if services:
                    services = services.replace(" ", "")
                    services = services.split(',')
                    if services:
                        services = Service.objects.filter(id__in=services) if Service.objects.filter(
                            id__in=services).exists() else None
                else:
                    services = None

            except Service.DoesNotExist:
                services = None

            try:
                if companies:
                    companies = companies.replace(" ", "")
                    companies = companies.split(',')
                    companies = Company.objects.filter(id__in=companies) if Company.objects.filter(
                        id__in=companies).exists() else None
                else:
                    companies = None
            except Company.DoesNotExist:
                companies = None

            if is_enable:
                offer.is_enable = True if is_enable == 'true' or is_enable == 'True' or is_enable == True else False
            if name:
                offer.name = name
            if coupon_code:
                offer.coupon_code = coupon_code
            if image:
                offer.image = image
            if discount_type:
                offer.discount_type = discount_type
            if discount_value:
                offer.discount_value = discount_value
            if up_to_amount:
                offer.up_to_amount = up_to_amount
            if redemption_type:
                offer.redemption_type = redemption_type
            if specify_no:
                offer.specify_no = specify_no
            if purchase_requirement:
                offer.purchase_requirement = True if purchase_requirement == 'true' or purchase_requirement == 'True' or purchase_requirement == True else False
            if min_purchase_amount:
                offer.min_purchase_amount = min_purchase_amount
            if allow_multiple_redeem:
                offer.allow_multiple_redeem = allow_multiple_redeem
            if multiple_redeem_specify_no:
                offer.multiple_redeem_specify_no = multiple_redeem_specify_no
            if on_home_screen:
                offer.on_home_screen = True if on_home_screen == 'true' or on_home_screen == 'True' or on_home_screen == True else False
            if on_checkout:
                offer.on_checkout = True if on_checkout == 'true' or on_checkout == 'True' or on_checkout == True else False
            if start_date:
                offer.start_date = start_date
            if end_date:
                offer.end_date = end_date
            if is_lifetime:
                offer.is_lifetime = is_lifetime
            if apply_global:
                offer.apply_global = True if apply_global == 'true' or apply_global == 'True' or apply_global == True else False

            if services:
                offer.services.set(services)
            if companies:
                offer.companies.set(companies)
            offer.save()

            # Get the updated Offer instance
            offer_after_update = Offer.objects.get(pk=kwargs['pk'])

            # Serialize the data after the update
            value_after = serialize('json', [offer_after_update])

            # Log the Offer update action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Offer",
                action='Updated',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Offer',
                action_value='Update',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            serializer = OfferSerializer(offer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class OfferServiceInfoView(generics.ListAPIView):
#     queryset = Offer.objects.all()
#     serializer_class = OfferServiceInfoSerializer

#     def retrieve(self, request, *args, **kwargs):

#         instance = self.get_object()
#         selected_services_count = instance.services.count()
#         selected_services_ids = list(instance.services.values_list('id', flat=True))

#         serializer = self.get_serializer({
#             'selected_services_count': selected_services_count,
#             'selected_services_ids': selected_services_ids
#         })

#         return Response(serializer.data)

class OfferServiceInfoView(generics.ListAPIView):
    serializer_class = OfferServiceInfoSerializer

    def get_queryset(self):
        offer_id = self.kwargs['pk']  # assuming you pass offer_id in the URL
        return Offer.objects.filter(id=offer_id)

    # def get_queryset(self):
    #     # Filter services based on the offer ID
    #     return Service.objects.filter(offer__offer_companies__isnull=False).distinct()


class OfferCountView(APIView):
    def get(self, request, *args, **kwargs):
        total_offers = Offer.objects.count()
        enabled_offers = Offer.objects.filter(is_enable=True).count()
        disabled_offers = Offer.objects.filter(is_enable=False).count()

        serializer = OfferCountSerializer({
            'total_offers': total_offers,
            'enabled_offers': enabled_offers,
            'disabled_offers': disabled_offers,
        })

        return Response(serializer.data)


#Export

class OfferListExportView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Offer.objects.all()
        resource = OfferListExportResource()

        dataset = resource.export(queryset)

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="offer_list.csv"'

        return response
