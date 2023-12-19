from rest_framework import serializers
from .models import Offer
from local_apps.service.serializers import ServiceSerializer
from local_apps.company.serializers import CompanySerializer
from local_apps.service.models import Service
from local_apps.company.models import Company


class OfferSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False, allow_null=True)
    companies = CompanySerializer(many=True, required=False, allow_null=True)
    class Meta:
        model = Offer
        fields = '__all__'


class OfferServiceInfoSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False, allow_null=True)
    companies = CompanySerializer(many=True, required=False, allow_null=True)
    company_service_count = serializers.SerializerMethodField()
    total_services = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = ['companies', 'services', 'company_service_count', 'total_services']

    def get_company_service_count(self, obj):
        companies = obj.companies.all()
        counts = []
        for company in companies:
            count = obj.services.filter(company=company).count()
            counts.append({
                'company_id': str(company.id),
                'service_count': count,
            })
        return counts
    def get_total_services(self, obj):
        companies = obj.companies.all()
        total_services = Service.objects.filter(company__in=companies).count()
        return total_services

class OfferCountSerializer(serializers.Serializer):
    total_offers = serializers.IntegerField()
    enabled_offers = serializers.IntegerField()
    disabled_offers = serializers.IntegerField()