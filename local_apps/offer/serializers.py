from rest_framework import serializers
from .models import Offer
from local_apps.service.serializers import ServiceSerializer
from local_apps.company.serializers import CompanySerializer
from local_apps.service.models import Service
from local_apps.company.models import Company
from import_export import resources, fields, widgets

from ..booking.models import Booking


class OfferSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False, allow_null=True)
    companies = CompanySerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['id','is_enable','name','coupon_code','image','discount_type','discount_value','up_to_amount','redemption_type','specify_no','purchase_requirement',
                  'min_purchase_amount','allow_multiple_redeem','multiple_redeem_specify_no','on_home_screen','on_checkout','start_date','end_date',
                  'is_lifetime','services','companies','apply_global']


class OfferServiceInfoSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False, allow_null=True)
    companies = CompanySerializer(many=True, required=False, allow_null=True)
    company_service_count = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = ['companies', 'services', 'company_service_count']

    def get_company_service_count(self, obj):
        companies = obj.companies.all()
        counts = []
        total_services = Service.objects.filter(company__in=companies).count()
        for company in companies:
            count = obj.services.filter(company=company).count()
            counts.append({
                'company_id': str(company.id),
                'service_count': count,
                'total_services': total_services,
            })
        return counts


class OfferCountSerializer(serializers.Serializer):
    total_offers = serializers.IntegerField()
    enabled_offers = serializers.IntegerField()
    disabled_offers = serializers.IntegerField()


class OfferListExportResource(resources.ModelResource):
    usage = fields.Field(column_name='usage', attribute='dehydrate_usage')

    def dehydrate_usage(self, instance):
        try:
            total_count = Booking.objects.filter(offer=instance).count()
            return total_count
        except:
            return 0

    class Meta:
        model = Offer
        fields = [
            "coupon_code",
            "name",
            "usage",
            "specify_no",
            "end_date",
        ]

        export_order = fields

