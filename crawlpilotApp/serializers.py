
from rest_framework import serializers
from .models import CrawledURL, CrawlingStatus

class CrawledURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawledURL
        fields = '__all__'

class CrawlingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlingStatus
        fields = '__all__'
