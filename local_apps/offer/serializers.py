from rest_framework import serializers
from .models import Offer
from local_apps.service.serializers import ServiceSerializer
from local_apps.company.serializers import CompanySerializer


class OfferSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False, allow_null=True)
    companies = CompanySerializer(many=True, required=False, allow_null=True)
    class Meta:
        model = Offer
        fields = '__all__'

#for the count of service
class OfferServiceInfoSerializer(serializers.Serializer):
    selected_services_count = serializers.IntegerField()
    selected_services_ids = serializers.ListField(child=serializers.UUIDField())