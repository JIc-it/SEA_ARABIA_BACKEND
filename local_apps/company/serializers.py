from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from local_apps.main.serializers import *

User = get_user_model()


class ServiceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTag
        exclude = ["created_at", "updated_at"]


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualifications
        exclude = ["created_at", "updated_at"]


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ["created_at", "updated_at", "prefix",
                   "first_two_letters", "first_two_numbers", "last_one_letter", "last_two_numbers"]


class CompanyAddSerializer(serializers.ModelSerializer):
    """serializer for adding and updating the company details in vendor"""

    service_summary = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "registration_number",
            "address",
            "website",
            "third_party_ownership",
            "service_summary",
        ]


class CompanyCmsSerializer(serializers.ModelSerializer):
    """ serializer for lisiting the company in the admin review cms """
    class Meta:
        model = Company
        fields = [
            "id",
            "company_id",
            "name"
        ]


class CompanyListSerializer(serializers.ModelSerializer):
    service_summary = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=ServiceTag.objects.all()
    )
    staffs = serializers.SlugRelatedField(
        many=True,
        slug_field="id",
        queryset=User.objects.all(),
    )
    user_first_name = serializers.CharField(
        source="user.first_name", allow_null=True)

    user_last_name = serializers.CharField(
        source="user.last_name", allow_null=True)
    created_by = serializers.SerializerMethodField(allow_null=True)\


    class Meta:
        model = Company
        exclude = ["created_at", "updated_at", "prefix",
                   "first_two_letters", "first_two_numbers", "last_one_letter", "last_two_numbers"]

    def get_created_by(self, instance):
        try:
            return f"{instance.user.first_name} {instance.user.last_name}"
        except:
            return "No Name"


class MiscellaneousSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField()
    status = serializers.CharField(
        source="company.status", default=None)

    class Meta:
        model = Miscellaneous
        exclude = [
            "created_at",
            "updated_at",
        ]


class MiscellaneousTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiscellaneousType
        exclude = [
            "created_at",
            "updated_at",
        ]


class SiteVisitSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=True)
    qualifications = serializers.ListField(required=False, write_only=True)
    status = serializers.CharField(
        source="company.status", default=None)

    class Meta:
        model = SiteVisit
        exclude = [
            "created_at",
            "updated_at",
        ]


class ProposalSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=True)
    status = serializers.CharField(
        source="company.status", default=None)

    class Meta:
        model = Proposal
        exclude = [
            "created_at",
            "updated_at",
        ]


class NegotiationSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=True)
    status = serializers.CharField(
        source="company.status", default=None)

    class Meta:
        model = Negotiation
        exclude = ["created_at", "updated_at"]


class MOUorCharterSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=True)
    status = serializers.CharField(
        source="company.status", default=None)

    class Meta:
        model = MOUorCharter
        exclude = ["created_at", "updated_at"]


class OnboardStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(
        source="company.status", default=None)

    class Meta:
        model = OnboardStatus
        fields = ["name", "status"]


class CompanyOnboardSerializer(serializers.Serializer):
    status = serializers.BooleanField()
