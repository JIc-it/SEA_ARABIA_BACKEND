from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

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
        exclude = ["created_at", "updated_at"]


class CompanyAddSerializer(serializers.ModelSerializer):
    """serializer for adding and updating the company details in vendor"""

    class Meta:
        model = Company
        fields = [
            "name",
            "registration_number",
            "address",
            "website",
            "third_party_ownership",
            "service_summary",
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

    class Meta:
        model = Company
        exclude = ["created_at", "updated_at"]


class MiscellaneousSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField()

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
    attachment = serializers.FileField()

    class Meta:
        model = SiteVisit
        exclude = [
            "created_at",
            "updated_at",
        ]


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        exclude = [
            "created_at",
            "updated_at",
        ]


class NegotiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negotiation
        exclude = ["created_at", "updated_at"]


class MOUorCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MOUorCharter
        exclude = ["created_at", "updated_at"]


class OnboardStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardStatus
        fields = ["name"]
