from rest_framework import serializers

from .models import Trim


class TrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trim
        fields = ["link"]
