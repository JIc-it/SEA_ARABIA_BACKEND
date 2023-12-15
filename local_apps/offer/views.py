from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from .models import Offer
from .serializers import OfferSerializer, OfferServiceInfoSerializer
from rest_framework.response import Response
from local_apps.service.models import Service
from local_apps.company.models import Company


class AdminOfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class BeastDealsOfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_queryset(self):
        try:
            return Offer.objects.filter(is_enable=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OfferCreateView(generics.CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def create(self, request, *args, **kwargs):
        try:
            is_enable = request.data.get('is_enable', False)
            name = request.data.get('name', None)
            coupon_code = request.data.get('coupon_code', None)
            image = request.FILES.get('image', None)
            discount_type = request.data.get('discount_type', None)
            discount_value = request.data.get('discount_value', None)
            max_redeem_amount = request.data.get('max_redeem_amount', None)
            max_redeem_count = request.data.get('max_redeem_count', None)
            min_grand_total = request.data.get('min_grand_total', None)
            allow_multiple_redeem = request.data.get('allow_multiple_redeem', None)
            allow_global_redeem = request.data.get('allow_global_redeem', None)
            display_global = request.data.get('display_global', None)
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)
            services = request.data.get('services', None)
            companies = request.data.get('companies', None)

            try:
                services = Service.objects.filter(id__in=services)
            except Service.DoesNotExist:
                services = None

            try:
                companies = Company.objects.filter(id__in=companies)
            except Company.DoesNotExist:
                companies = None

            offer = Offer.objects.create(
                is_enable=is_enable,
                name=name,
                coupon_code=coupon_code,
                image=image,
                discount_type=discount_type,
                discount_value=discount_value,
                max_redeem_amount=max_redeem_amount,
                max_redeem_count=max_redeem_count,
                min_grand_total=min_grand_total,
                allow_multiple_redeem=allow_multiple_redeem,
                allow_global_redeem=allow_global_redeem,
                display_global=display_global,
                start_date=start_date,
                end_date=end_date, )
            offer.services.set(services)
            offer.companies.set(companies)
            offer.save()
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
 
            offer = Offer.objects.get(pk=kwargs['pk'])

            is_enable = request.data.get('is_enable', False)
            name = request.data.get('name', None)
            coupon_code = request.data.get('coupon_code', None)
            image = request.data.get('image', None)
            discount_type = request.data.get('discount_type', None)
            discount_value = request.data.get('discount_value', None)
            max_redeem_amount = request.data.get('max_redeem_amount', None)
            max_redeem_count = request.data.get('max_redeem_count', None)
            min_grand_total = request.data.get('min_grand_total', None)
            allow_multiple_redeem = request.data.get('allow_multiple_redeem', None)
            allow_global_redeem = request.data.get('allow_global_redeem', None)
            display_global = request.data.get('display_global', None)
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)
            services = request.data.get('services', [])
            companies = request.data.get('companies', None)

            try:
                if services:
                    services = Service.objects.filter(id__in=services) if Service.objects.filter(id__in=services).exists() else None
                else:
                    services = None
                
            except Service.DoesNotExist:
                services = None

            try:
                if companies:
                    companies = Company.objects.filter(id__in=companies) if Company.objects.filter(id__in=companies).exists() else None
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
            if max_redeem_amount:
                offer.max_redeem_amount = max_redeem_amount
            if max_redeem_count:
                offer.max_redeem_count = max_redeem_count
            if min_grand_total:
                offer.min_grand_total = min_grand_total
            if allow_multiple_redeem:
                offer.allow_multiple_redeem = allow_multiple_redeem
            if allow_global_redeem:
                offer.allow_global_redeem = allow_global_redeem
            if display_global:
                offer.display_global = display_global
            if start_date:
                offer.start_date = start_date
            if end_date:
                offer.end_date = end_date
            if services:
                offer.services.set(services)
            if companies:
                offer.companies.set(companies)
            offer.save()
            serializer = OfferSerializer(offer)
            return Response(serializer.data, status=status.HTTP_200_OK)
    

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

           