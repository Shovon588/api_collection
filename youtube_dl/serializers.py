from rest_framework import serializers


class YoutubeDLSerializer(serializers.Serializer):
    url = serializers.URLField()
