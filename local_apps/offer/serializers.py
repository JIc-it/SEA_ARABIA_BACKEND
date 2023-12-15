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

    # Add a field to store the count of services for each company
    company_service_count = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = '__all__'

    def get_company_service_count(self, obj):
        # Assuming 'companies' is the related name in the Offer model for the ManyToManyField
        companies = obj.companies.all()
        counts = {}

        # Iterate through each company and get the count of services
        for company in companies:
            count = obj.services.filter(company=company).count()
            counts[str(company.id)] = count

        return counts



