from rest_framework import serializers

from app.models import Youtube


class YoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtube
        fields = '__all__'
