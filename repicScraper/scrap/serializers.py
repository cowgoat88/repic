from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'title', 'score', 'url', 'mp4', 'nsfw', 'sitetag')