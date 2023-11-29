from rest_framework import serializers
from .models import *


class ServiceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTag
        exclude = ["created_at", "updated_at"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ["created_at", "updated_at"]


class MiscellaneousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miscellaneous
        exclude = ["created_at", "updated_at"]


class SiteVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteVisit
        exclude = ["created_at", "updated_at"]


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        exclude = ["created_at", "updated_at"]


class NegotiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negotiation
        exclude = ["created_at", "updated_at"]


class MOUorCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MOUorCharter
        exclude = ["created_at", "updated_at"]
