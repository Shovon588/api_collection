from rest_framework import serializers

from .models import Trim


class TrimSerializer(serializers.ModelSerializer):
    alias = serializers.CharField(max_length=16, required=False)
    class Meta:
        model = Trim
        fields = ["link", "alias"]
